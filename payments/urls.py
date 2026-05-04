from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Payment verification endpoint (callback from Paystack)
    path('verify/', views.verify_payment_view, name='verify_payment'),

    # Webhook for Paystack to send transaction updates
    path('webhook/', views.paystack_webhook, name='webhook'),

    # Payment success page
    path('success/', views.payment_success, name='success'),

    # Payment cancelled/failed page
    path('cancelled/', views.payment_cancelled, name='cancelled'),

    # Initialize payment (alternative direct endpoint)
    path('initialize/<str:order_id>/', views.initialize_payment_view, name='initialize'),
]
