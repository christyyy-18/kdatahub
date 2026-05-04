from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
import uuid

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, editable=False)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_email = models.EmailField(blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    item_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    paystack_reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def carrier(self):
        name = self.item_name.upper()
        if 'MTN' in name:
            return 'MTN'
        if 'AIRTEL' in name or 'AT' in name:
            return 'AIRTEL'
        if 'TELECEL' in name:
            return 'TELECEL'
        return 'GENERAL'
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = f"KDH-{uuid.uuid4().hex[:8].upper()}"
        self.total_amount = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        buyer_name = self.buyer.username if self.buyer else self.customer_name
        return f"{self.order_id} - {buyer_name}"