from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order management
    path('create/', views.create_order, name='create_order'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('track/', views.track_order, name='track_order'),
    path('detail/<str:order_id>/', views.order_detail, name='order_detail'),
    
    # Manager endpoints
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('all-orders/', views.all_orders, name='all_orders'),
    
    # Order status updates (manager only)
    path('update-status/<str:order_id>/', views.update_order_status, name='update_status'),
    
    # Cancel order (buyer)
    path('cancel/<str:order_id>/', views.cancel_order, name='cancel_order'),
    
    # Invoice download
    path('invoice/<str:order_id>/', views.download_invoice, name='invoice'),
    
    # Search and filter orders
    path('search/', views.search_orders, name='search_orders'),
    
    # Export orders (manager only)
    path('export/', views.export_orders, name='export_orders'),
]