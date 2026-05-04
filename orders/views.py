from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from .models import Order
from payments.utils import initialize_payment
import csv
from django.utils.dateparse import parse_date
from kdatahub.sms import (
    notify_buyer_order_placed, 
    notify_manager_new_order, 
    notify_buyer_order_delivered,
    notify_admin_traffic
)

def is_manager(user):
    return user.is_authenticated and user.is_manager

def create_order(request):
    if request.method == 'POST':
        # Traffic detection: Check if more than 5 orders in the last 5 minutes
        five_mins_ago = timezone.now() - timezone.timedelta(minutes=5)
        recent_count = Order.objects.filter(created_at__gte=five_mins_ago).count()
        if recent_count >= 5:
            notify_admin_traffic(f"High traffic detected! {recent_count} orders in the last 5 minutes.")

        item_name = request.POST.get('item_name')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        
        try:
            quantity = int(request.POST.get('quantity', 1))
            unit_price = float(request.POST.get('unit_price', 0))
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity or unit price.')
            return render(request, 'orders/create_order.html')
        
        if not item_name or quantity < 1 or unit_price <= 0 or not customer_email or not customer_phone:
            messages.error(request, 'Please provide all required valid order details.')
            return render(request, 'orders/create_order.html')
        
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
        else:
            messages.error(request, 'Payment initialization failed. Please try again.')
            return redirect('orders:create_order')
    
    return render(request, 'orders/create_order.html')

@login_required
def my_orders(request):
    orders = Order.objects.filter(buyer=request.user).order_by('-created_at')
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/my_orders.html', {'orders': page_obj})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    
    if order.buyer and order.buyer != request.user and not request.user.is_manager:
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
    
    return redirect(request.META.get('HTTP_REFERER', 'orders:manager_dashboard'))

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
    
    # Security check
    if order.buyer != request.user and not request.user.is_manager:
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
    writer.writerow(['Buyer:', order.buyer.username])
    writer.writerow(['Email:', order.buyer.email])
    writer.writerow(['Item:', order.item_name])
    writer.writerow(['Quantity:', order.quantity])
    writer.writerow(['Unit Price:', f'₦{order.unit_price}'])
    writer.writerow(['Total Amount:', f'₦{order.total_amount}'])
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
            order.buyer.username,
            order.buyer.email,
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
    query = request.GET.get('ticket_id', '')
    order = None
    if query:
        order = Order.objects.filter(order_id__iexact=query).first()
    return render(request, 'orders/track_order.html', {'order': order, 'query': query})

