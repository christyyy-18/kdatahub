"""Shared logic for moving an order to `paid`.

Both the browser callback and the Paystack webhook funnel through
`mark_order_paid` so the same checks apply no matter which arrives first:

* the amount and currency Paystack actually charged must match the order
* the transition happens once, under a row lock, so Paystack's webhook retries
  do not re-run fulfilment or re-send the SMS
"""

import hashlib
import hmac
import logging

from django.conf import settings
from django.db import transaction

from orders.models import Order

from .utils import verify_payment

logger = logging.getLogger(__name__)

# Outcomes of mark_order_paid()
PAID = 'paid'
ALREADY_PROCESSED = 'already_processed'
NOT_FOUND = 'not_found'
FAILED = 'failed'


def signature_is_valid(request):
    """Check the x-paystack-signature HMAC over the raw request body."""
    secret = getattr(settings, 'PAYSTACK_SECRET_KEY', '')
    if not secret:
        logger.error('Paystack webhook received but PAYSTACK_SECRET_KEY is not set.')
        return False

    sent = request.headers.get('x-paystack-signature', '')
    if not sent:
        return False

    expected = hmac.new(
        secret.encode('utf-8'), request.body, hashlib.sha512
    ).hexdigest()
    return hmac.compare_digest(expected, sent)


def mark_order_paid(reference):
    """Confirm a payment with Paystack and flip the order to paid.

    Returns one of PAID / ALREADY_PROCESSED / NOT_FOUND / FAILED, plus the
    order (or None). The caller decides what to show the customer.
    """
    if not reference:
        return FAILED, None

    try:
        order = Order.objects.get(order_id=reference)
    except Order.DoesNotExist:
        logger.warning('Payment callback for unknown reference %s', reference)
        return NOT_FOUND, None

    if order.status != 'pending':
        # Paystack retries webhooks; a second delivery must be a no-op.
        return ALREADY_PROCESSED, order

    verification = verify_payment(reference) or {}
    if not verification.get('status'):
        logger.warning('Paystack verification call failed for %s', reference)
        return FAILED, order

    data = verification.get('data') or {}
    expected_amount = int(order.total_amount * 100)

    if data.get('status') != 'success':
        logger.info('Paystack reports %s for %s', data.get('status'), reference)
        return FAILED, order
    if data.get('amount') != expected_amount:
        logger.error(
            'Amount mismatch for %s: Paystack charged %s, order expects %s',
            reference, data.get('amount'), expected_amount,
        )
        return FAILED, order
    if data.get('currency') != 'GHS':
        logger.error('Currency mismatch for %s: %s', reference, data.get('currency'))
        return FAILED, order

    with transaction.atomic():
        locked = Order.objects.select_for_update().get(pk=order.pk)
        if locked.status != 'pending':
            return ALREADY_PROCESSED, locked
        locked.status = 'paid'
        locked.paystack_reference = reference
        locked.save(update_fields=['status', 'paystack_reference', 'updated_at'])

    return PAID, locked
