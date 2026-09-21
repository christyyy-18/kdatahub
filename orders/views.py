from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.utils.http import url_has_allowed_host_and_scheme
from .models import Order
from . import catalog
from payments.utils import initialize_payment
import csv
import re
from django.utils.dateparse import parse_date
from kdatahub.throttle import is_rate_limited
from kdatahub.sms import (
    notify_buyer_order_placed, 
    notify_manager_new_order, 
    notify_buyer_order_delivered,
    notify_admin_traffic
)

def is_manager(user):
    return user.is_authenticated and user.is_manager


# Ghana mobile numbers: 10 digits starting 0, or the same with a 233 prefix.
PHONE_RE = re.compile(r'^(?:0\d{9}|(?:\+?233)\d{9})$')


def _order_form_context(request, selected_key=None, form_data=None):
    """Everything create_order.html needs, for both GET and any error re-render."""
    is_agent = getattr(request.user, 'is_agent', False)
    if selected_key is not None and not catalog.is_valid_package(selected_key):
        selected_key = None
    selected_price = (
        catalog.get_price(selected_key, is_agent=is_agent) if selected_key else None
    )
    return {
        'catalog': catalog.catalog_for(is_agent=is_agent),
        'price_map': catalog.price_map(is_agent=is_agent),
        'selected_key': selected_key,
        'selected_price': selected_price,
        'max_quantity': catalog.MAX_QUANTITY,
        'form_data': form_data or {},
    }


def create_order(request):
    if request.method != 'POST':
        # A price box on the home page links here with ?package=10GB MTN so the
        # plan the customer picked arrives already selected. An unrecognised
        # value is simply ignored.
        context = _order_form_context(request, selected_key=request.GET.get('package'))
        return render(request, 'orders/create_order.html', context)

    item_name = (request.POST.get('item_name') or '').strip()
    customer_name = (request.POST.get('customer_name') or '').strip()
    customer_email = (request.POST.get('customer_email') or '').strip()
    customer_phone = (request.POST.get('customer_phone') or '').strip()
    form_data = {
        'customer_name': customer_name,
        'customer_email': customer_email,
        'customer_phone': customer_phone,
    }

    def reject(message):
        messages.error(request, message)
        return render(
            request,
            'orders/create_order.html',
            _order_form_context(request, selected_key=item_name, form_data=form_data),
        )

    if is_rate_limited(request, 'create_order', limit=5, window_seconds=300):
        return reject('Too many orders from this device. Please wait a few minutes and try again.')

    # The price is looked up here, never read from the request. The form has no
    # price field at all: a buyer cannot choose what they pay.
    is_agent = getattr(request.user, 'is_agent', False)
    unit_price = catalog.get_price(item_name, is_agent=is_agent)
    if unit_price is None:
        return reject('Please choose a data package from the list.')

    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        return reject('Please enter a valid quantity.')
    if quantity < 1 or quantity > catalog.MAX_QUANTITY:
        return reject(f'Quantity must be between 1 and {catalog.MAX_QUANTITY}.')

    if not customer_email:
        return reject('Please provide an email address for your receipt.')
    try:
        validate_email(customer_email)
    except ValidationError:
        return reject('Please provide a valid email address.')

    if not PHONE_RE.match(customer_phone.replace(' ', '')):
        return reject('Please provide a valid Ghana phone number, e.g. 0241234567.')

    if not customer_name:
        return reject('Please provide your full name.')

    # Traffic detection: Check if more than 5 orders in the last 5 minutes
    five_mins_ago = timezone.now() - timezone.timedelta(minutes=5)
    recent_count = Order.objects.filter(created_at__gte=five_mins_ago).count()
    if recent_count >= 5:
        notify_admin_traffic(f"High traffic detected! {recent_count} orders in the last 5 minutes.")

    buyer = request.user if request.user.is_authenticated else None

    order = Order.objects.create(
        buyer=buyer,
        customer_name=customer_name,
        customer_email=customer_email,
        customer_phone=customer_phone,
        item_name=item_name,
        quantity=quantity,
        unit_price=unit_price,
        status='pending'
    )

    # Trigger SMS Notifications
    notify_buyer_order_placed(order)
    notify_manager_new_order(order)

    payment_response = initialize_payment(order, customer_email)

    if payment_response and payment_response.get('status'):
        order.paystack_reference = payment_response['data']['reference']
        order.save()
        return redirect(payment_response['data']['authorization_url'])

    messages.error(request, 'Payment initialization failed. Please try again.')
    return redirect('orders:create_order')


@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/my_orders.html', {'orders': page_obj})

def _may_view_order(user, order):
    """Guest orders have no buyer, so only a manager may open them."""
    if user.is_manager:
        return True
    return order.buyer is not None and order.buyer == user


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if not _may_view_order(request.user, order):
        messages.error(request, 'Permission denied.')
        return redirect('orders:my_orders')

    return render(request, 'orders/order_detail.html', {'order': order})

@user_passes_test(is_manager)
def manager_dashboard(request):
    today = timezone.now().date()
    today_orders = Order.objects.filter(created_at__date=today)
    
    # Get current week orders
    week_start = today - timezone.timedelta(days=today.weekday())
    week_orders = Order.objects.filter(created_at__date__gte=week_start)
    
    # Get current month orders
    month_orders = Order.objects.filter(created_at__year=today.year, created_at__month=today.month)
    
    # Get top products
    top_products = Order.objects.filter(status='paid').values('item_name').annotate(
        total_quantity=models.Sum('quantity')
    ).order_by('-total_quantity')[:5]
    
    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:20]
    
    # Get status distribution
    status_distribution = {
        'pending': Order.objects.filter(status='pending').count(),
        'paid': Order.objects.filter(status='paid').count(),
        'processing': Order.objects.filter(status='processing').count(),
        'completed': Order.objects.filter(status='completed').count(),
        'cancelled': Order.objects.filter(status='cancelled').count(),
    }
    # Calculate last 7 days revenue for chart
    last_7_days_labels = []
    last_7_days_revenue = []
    for i in range(6, -1, -1):
        day = today - timezone.timedelta(days=i)
        day_orders = Order.objects.filter(created_at__date=day, status='paid')
        revenue = day_orders.aggregate(total=models.Sum('total_amount'))['total'] or 0
        last_7_days_labels.append(day.strftime('%b %d'))
        last_7_days_revenue.append(float(revenue))
    
    context = {
        'total_orders_today': today_orders.count(),
        'total_revenue_today': today_orders.filter(status='paid').aggregate(total=models.Sum('total_amount'))['total'] or 0,
        'pending_orders': today_orders.filter(status='pending').count(),
        'completed_orders': today_orders.filter(status='completed').count(),
        'week_orders': week_orders.count(),
        'week_revenue': week_orders.filter(status='paid').aggregate(total=models.Sum('total_amount'))['total'] or 0,
        'month_orders': month_orders.count(),
        'month_revenue': month_orders.filter(status='paid').aggregate(total=models.Sum('total_amount'))['total'] or 0,
        'top_products': top_products,
        'recent_orders': recent_orders,
        'status_distribution': status_distribution,
        'last_7_days_labels': last_7_days_labels,
        'last_7_days_revenue': last_7_days_revenue,
    }
    return render(request, 'orders/manager_dashboard.html', context)

@user_passes_test(is_manager)
def all_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Filter by date range
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        orders = orders.filter(created_at__date__gte=parse_date(date_from))
    if date_to:
        orders = orders.filter(created_at__date__lte=parse_date(date_to))
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        orders = orders.filter(
            models.Q(order_id__icontains=search_query) |
            models.Q(buyer__username__icontains=search_query) |
            models.Q(item_name__icontains=search_query)
        )
    
    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/all_orders.html', {'orders': page_obj, 'status_filter': status_filter})

@user_passes_test(is_manager)
def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, order_id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Order.STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
            
            # Trigger SMS if delivered
            if new_status == 'completed':
                notify_buyer_order_delivered(order)
                
            messages.success(request, f'Order {order.order_id} status updated to {order.get_status_display()}')
        else:
            messages.error(request, 'Invalid status')
    
    referer = request.META.get('HTTP_REFERER')
    if referer and url_has_allowed_host_and_scheme(
        referer, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(referer)
    return redirect('orders:manager_dashboard')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id, buyer=request.user)
    
    # Only pending orders can be cancelled
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, f'Order {order.order_id} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('orders:my_orders')

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if not _may_view_order(request.user, order):
        messages.error(request, 'Permission denied')
        return redirect('orders:my_orders')
    
    # Create CSV invoice (simple version)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.order_id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['K-DATA HUB - INVOICE'])
    writer.writerow([])
    writer.writerow(['Order ID:', order.order_id])
    writer.writerow(['Date:', order.created_at.strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow(['Buyer:', order.buyer.username if order.buyer else (order.customer_name or 'Guest')])
    writer.writerow(['Email:', order.buyer.email if order.buyer else (order.customer_email or '')])
    writer.writerow(['Item:', order.item_name])
    writer.writerow(['Quantity:', order.quantity])
    writer.writerow(['Unit Price:', f'GHS {order.unit_price}'])
    writer.writerow(['Total Amount:', f'GHS {order.total_amount}'])
    writer.writerow(['Status:', order.get_status_display()])
    writer.writerow(['Paystack Reference:', order.paystack_reference or 'N/A'])
    
    return response

@login_required
def search_orders(request):
    query = request.GET.get('q', '')
    if not query:
        return redirect('orders:my_orders')
    
    orders = Order.objects.filter(buyer=request.user).filter(
        models.Q(order_id__icontains=query) |
        models.Q(item_name__icontains=query)
    ).order_by('-created_at')
    
    return render(request, 'orders/my_orders.html', {'orders': orders, 'search_query': query})

@user_passes_test(is_manager)
def export_orders(request):
    """Export all orders to CSV"""
    orders = Order.objects.all().order_by('-created_at')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_orders_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Buyer', 'Email', 'Item', 'Quantity', 'Unit Price', 'Total', 'Status', 'Date', 'Paystack Ref'])
    
    for order in orders:
        writer.writerow([
            order.order_id,
            order.buyer.username if order.buyer else (order.customer_name or 'Guest'),
            order.buyer.email if order.buyer else (order.customer_email or ''),
            order.item_name,
            order.quantity,
            order.unit_price,
            order.total_amount,
            order.get_status_display(),
            order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            order.paystack_reference or ''
        ])
    
    return response
def track_order(request):
    query = request.GET.get('ticket_id', '').strip()
    order = None

    if query:
        if is_rate_limited(request, 'track_order', limit=15, window_seconds=300):
            messages.error(request, 'Too many lookups. Please wait a few minutes and try again.')
            return render(request, 'orders/track_order.html', {'order': None, 'query': query})
        order = Order.objects.filter(order_id__iexact=query).first()

    return render(request, 'orders/track_order.html', {
        'order': order,
        'query': query,
        # Anyone holding an order ID can reach this page, so the contact
        # details are masked unless it is the buyer's own order.
        'show_full_contact': bool(
            order
            and request.user.is_authenticated
            and (request.user.is_manager or order.buyer == request.user)
        ),
    })

