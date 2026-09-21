from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .utils import initialize_payment
from .services import (
    mark_order_paid,
    signature_is_valid,
    PAID,
    ALREADY_PROCESSED,
    NOT_FOUND,
)
import json
import logging
from kdatahub.sms import notify_buyer_payment_success

logger = logging.getLogger(__name__)


def verify_payment_view(request):
    """Where Paystack sends the customer's browser after checkout."""
    reference = request.GET.get('reference')
    if not reference:
        return redirect('orders:track_order')

    outcome, order = mark_order_paid(reference)

    if outcome == PAID:
        notify_buyer_payment_success(order)
        messages.success(request, f'Payment successful! Your order {order.order_id} is confirmed.')
    elif outcome == ALREADY_PROCESSED:
        messages.info(request, f'Order {order.order_id} is already confirmed.')
    elif outcome == NOT_FOUND:
        messages.error(request, 'Order not found.')
    else:
        messages.error(request, 'Payment verification failed. If you were charged, contact support.')

    return redirect(f'/orders/track/?ticket_id={reference}')


def payment_success(request):
    messages.success(request, 'Payment completed successfully.')
    return redirect('orders:track_order')


def payment_cancelled(request):
    messages.warning(request, 'Payment was cancelled or failed.')
    return redirect('orders:track_order')


@csrf_exempt
def paystack_webhook(request):
    """Server-to-server payment notification from Paystack.

    CSRF is exempt because the signature header is what authenticates this
    request, so it has to be checked before anything else happens.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    if not signature_is_valid(request):
        logger.warning('Rejected Paystack webhook with a missing or invalid signature.')
        return HttpResponse('Invalid signature.', status=401)

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, UnicodeDecodeError):
        return HttpResponseBadRequest('Invalid JSON payload.')

    if payload.get('event') == 'charge.success':
        reference = (payload.get('data') or {}).get('reference')
        outcome, order = mark_order_paid(reference)
        if outcome == PAID:
            notify_buyer_payment_success(order)

    # Always 200 on a validly signed request, so Paystack stops retrying.
    return JsonResponse({'status': 'ok'})


def initialize_payment_view(request, order_id):
    if request.method != 'GET':
        return HttpResponseBadRequest('Invalid request method.')

    order = get_object_or_404(Order, order_id=order_id)

    # Only the person who placed the order (or a manager) may start a payment
    # for it -- otherwise anyone with an order ID could overwrite its reference.
    is_manager = getattr(request.user, 'is_manager', False)
    if not is_manager and (order.buyer is None or order.buyer != request.user):
        messages.error(request, 'Permission denied.')
        return redirect('home')

    if order.status != 'pending':
        messages.warning(request, 'This order cannot be initialized for payment.')
        return redirect('orders:order_detail', order_id=order_id)

    email_to_use = order.customer_email
    if not email_to_use:
        email_to_use = request.user.email if request.user.is_authenticated else (order.buyer.email if order.buyer else '')
    payment_response = initialize_payment(order, email_to_use)
    if payment_response and payment_response.get('status'):
        order.paystack_reference = payment_response['data'].get('reference')
        order.save()
        return redirect(payment_response['data'].get('authorization_url'))

    messages.error(request, 'Payment initialization failed. Please try again.')
    return redirect('orders:order_detail', order_id=order_id)
