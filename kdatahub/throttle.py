"""A small cache-backed rate limiter.

Used to slow down the endpoints an anonymous visitor can hit repeatedly:
manager login (password guessing), order creation (each one sends billable
SMS and opens a Paystack transaction) and order tracking (order-ID guessing).

Counters live in the shared cache rather than in memory, so they still hold
when the app runs as several serverless instances.
"""

import logging

from django.core.cache import cache

logger = logging.getLogger(__name__)


def client_ip(request):
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        # Vercel appends the real client IP first.
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def is_rate_limited(request, scope, limit, window_seconds):
    """Record a hit and report whether this client has gone over `limit`.

    Fails open: if the cache backend is unavailable the request is allowed
    through rather than taking the site down.
    """
    key = f'throttle:{scope}:{client_ip(request)}'
    try:
        added = cache.add(key, 1, window_seconds)
        count = 1 if added else cache.incr(key)
    except ValueError:
        # The key expired between add() and incr(); treat as a fresh window.
        cache.set(key, 1, window_seconds)
        return False
    except Exception:
        logger.exception('Rate limit check failed for scope %s', scope)
        return False
    return count > limit
