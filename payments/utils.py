import requests
from django.conf import settings
import json

def initialize_payment(order, email):
    url = 'https://api.paystack.co/transaction/initialize'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
        'Content-Type': 'application/json',
    }
    callback_url = f'{settings.BASE_DOMAIN}/payments/verify/'
    payload = {
        'email': email,
        'amount': int(order.total_amount * 100),  # Convert to kobo
        'reference': order.order_id,
        'callback_url': callback_url,
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

def verify_payment(reference):
    url = f'https://api.paystack.co/transaction/verify/{reference}'
    headers = {
        'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
    }
    
    response = requests.get(url, headers=headers)
    return response.json()