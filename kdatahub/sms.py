import requests
import logging
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)

def send_sms(phone, message):
    """
    Sends an SMS via Arkesel API.
    If ARKESEL_API_KEY is not set, it defaults to Mock Mode (console print).
    """
    api_key = getattr(settings, 'ARKESEL_API_KEY', '')
    sender_id = getattr(settings, 'SMS_SENDER_ID', 'K-DATAHUB')
    
    # Clean phone number and ensure Ghana country code (233)
    clean_phone = "".join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith('0'):
        clean_phone = '233' + clean_phone[1:]
    elif not clean_phone.startswith('233') and len(clean_phone) <= 10:
        clean_phone = '233' + clean_phone
    
    if not api_key:
        print("\n" + "="*50)
        print("MOCK SMS NOTIFICATION")
        print(f"TO: {clean_phone}")
        print(f"MESSAGE: {message}")
        print("="*50 + "\n")
        return True

    url = "https://sms.arkesel.com/api/v2/sms/send"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "sender": sender_id,
        "message": message,
        "recipients": [clean_phone]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        # Arkesel v2 success code is 200/201 in HTTP, but response body contains status
        if result.get('status') == 'success' or response.status_code in [200, 201]:
            logger.info(f"SMS successfully sent to {clean_phone}")
            return True
        else:
            logger.error(f"Arkesel Error: {result.get('message') or result}")
            return False
    except Exception as e:
        logger.error(f"SMS Sending Failed: {str(e)}")
        return False

# --- Helper Functions for Specific Scenarios ---

def notify_buyer_order_placed(order):
    phone = order.customer_phone
    if not phone and order.buyer:
        phone = getattr(order.buyer, 'phone_number', '') # Assuming phone_number field exists
    
    if phone:
        message = (
            f"K-DATA HUB: Order {order.order_id} received for {order.item_name} (₵{order.total_amount}). "
            f"Please complete payment to begin processing. Track here: {settings.BASE_DOMAIN}/orders/track/?ticket_id={order.order_id}"
        )
        send_sms(phone, message)

def notify_buyer_payment_success(order):
    phone = order.customer_phone
    if not phone and order.buyer:
        phone = getattr(order.buyer, 'phone_number', '')
    
    if phone:
        # This is the 'Ticket Receipt' requested by the user
        message = (
            f"K-DATA HUB RECEIPT: Payment Received! \n"
            f"Ticket: {order.order_id}\n"
            f"Package: {order.item_name}\n"
            f"Status: Paid & Processing for delivery to {phone}. \n"
            f"Thank you for your order!"
        )
        send_sms(phone, message)

def notify_buyer_order_delivered(order):
    phone = order.customer_phone
    if not phone and order.buyer:
        phone = getattr(order.buyer, 'phone_number', '')
    
    if phone:
        message = f"Hi {order.customer_name or 'Customer'}, your order {order.order_id} ({order.item_name}) has been successfully delivered! Thank you for choosing K-DATA HUB."
        send_sms(phone, message)

def notify_manager_new_order(order):
    manager_phone = getattr(settings, 'MANAGER_PHONE', '')
    if manager_phone:
        message = f"NEW ORDER: {order.order_id} | {order.item_name} | ₵{order.total_amount} | Buyer: {order.customer_name or 'Guest'}"
        send_sms(manager_phone, message)

def notify_manager_login(user):
    manager_phone = getattr(settings, 'MANAGER_PHONE', '')
    if manager_phone:
        time_str = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"SECURITY ALERT: Manager {user.username} successfully logged in at {time_str}."
        send_sms(manager_phone, message)

def notify_manager_agent_signup(user):
    manager_phone = getattr(settings, 'MANAGER_PHONE', '')
    if manager_phone:
        message = f"AGENT SIGNUP: {user.username} has registered as a new agent on K-DATA HUB."
        send_sms(manager_phone, message)

def notify_agent_welcome(user):
    # Assuming user.phone_number exists
    phone = getattr(user, 'phone_number', '')
    if phone:
        message = f"Congratulations {user.username}! Your agent account is now active. You can now place orders at discounted prices. Welcome to K-DATA HUB!"
        send_sms(phone, message)

def notify_admin_traffic(details):
    admin_phone = getattr(settings, 'ADMIN_PHONE', '')
    if admin_phone:
        message = f"TRAFFIC ALERT: {details}"
        send_sms(admin_phone, message)
