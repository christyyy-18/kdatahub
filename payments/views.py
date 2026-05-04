from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .utils import initialize_payment, verify_payment
import json
from kdatahub.sms import notify_buyer_payment_success

# Create your views here.

def verify_payment_view(request):
    reference = request.GET.get('reference')
    if reference:
        verification = verify_payment(reference)
        if verification.get('status') and verification['data']['status'] == 'success':
            order_id = reference
            try:
                order = Order.objects.get(order_id=order_id)
                order.status = 'paid'
                order.save()
                
                # Trigger SMS Notification
                notify_buyer_payment_success(order)
                
                if order.item_name == 'Agent Registration Fee':
                    order.buyer.is_agent = True
                    order.buyer.save()
                    from accounts.models import AgentRequest
                    agent_request = AgentRequest.objects.filter(user=order.buyer, status='pending').first()
                    if agent_request:
                        agent_request.status = 'approved'
                        agent_request.save()
                    messages.success(request, 'Payment successful! You are now registered as an Agent.')
                else:
                    messages.success(request, f'Payment successful! Your order {order.order_id} is confirmed.')
                return redirect(f'/orders/track/?ticket_id={order_id}')
            except Order.DoesNotExist:
                messages.error(request, 'Order not found.')
        else:
            messages.error(request, 'Payment verification failed.')
        return redirect(f'/orders/track/?ticket_id={reference}')
    return redirect('orders:track_order')


def payment_success(request):
    messages.success(request, 'Payment completed successfully.')
    return redirect('orders:track_order')


def payment_cancelled(request):
    messages.warning(request, 'Payment was cancelled or failed.')
    return redirect('orders:track_order')


@csrf_exempt
def paystack_webhook(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method.')

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except (ValueError, json.JSONDecodeError):
        return HttpResponseBadRequest('Invalid JSON payload.')

    event = payload.get('event')
    data = payload.get('data', {})
    if event == 'charge.success' and data.get('status') == 'success':
        reference = data.get('reference')
        if reference:
            order_id = reference
            try:
                order = Order.objects.get(order_id=order_id)
                order.status = 'paid'
                order.paystack_reference = reference
                order.save()
                
                # Trigger SMS Notification
                notify_buyer_payment_success(order)
                
                if order.item_name == 'Agent Registration Fee':
                    order.buyer.is_agent = True
                    order.buyer.save()
                    from accounts.models import AgentRequest
                    agent_request = AgentRequest.objects.filter(user=order.buyer, status='pending').first()
                    if agent_request:
                        agent_request.status = 'approved'
                        agent_request.save()
            except Order.DoesNotExist:
                pass

    return JsonResponse({'status': 'ok'})


def initialize_payment_view(request, order_id):
    if request.method != 'GET':
        return HttpResponseBadRequest('Invalid request method.')

    order = get_object_or_404(Order, order_id=order_id)
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