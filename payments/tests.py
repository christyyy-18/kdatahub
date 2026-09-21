import hashlib
import hmac
import json
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from orders.models import Order

SECRET = 'sk_test_unit_test_key'


def paystack_success(amount, currency='GHS'):
    return {'status': True, 'data': {'status': 'success', 'amount': amount, 'currency': currency}}


def sign(body):
    return hmac.new(SECRET.encode('utf-8'), body, hashlib.sha512).hexdigest()


@override_settings(PAYSTACK_SECRET_KEY=SECRET)
@patch('payments.views.notify_buyer_payment_success', lambda *a, **k: None)
class PaystackWebhookTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            customer_name='Ama Mensah',
            customer_email='ama@example.com',
            customer_phone='0241234567',
            item_name='10GB MTN',
            quantity=1,
            unit_price=Decimal('50.00'),
        )
        self.url = reverse('payments:webhook')

    def payload(self, reference=None):
        return json.dumps({
            'event': 'charge.success',
            'data': {'status': 'success', 'reference': reference or self.order.order_id},
        }).encode()

    def post(self, body, signature=None):
        headers = {}
        if signature is not None:
            headers['HTTP_X_PAYSTACK_SIGNATURE'] = signature
        return self.client.post(
            self.url, data=body, content_type='application/json', **headers
        )

    def test_unsigned_webhook_is_rejected(self):
        response = self.post(self.payload())

        self.assertEqual(response.status_code, 401)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')

    def test_wrongly_signed_webhook_is_rejected(self):
        response = self.post(self.payload(), signature='deadbeef')

        self.assertEqual(response.status_code, 401)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')

    def test_signed_webhook_marks_the_order_paid(self):
        body = self.payload()
        with patch('payments.services.verify_payment', return_value=paystack_success(5000)):
            response = self.post(body, signature=sign(body))

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')

    def test_underpayment_does_not_mark_the_order_paid(self):
        """A real but tiny payment must not settle a GHS 50 order."""
        body = self.payload()
        with patch('payments.services.verify_payment', return_value=paystack_success(1)):
            response = self.post(body, signature=sign(body))

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')

    def test_wrong_currency_does_not_mark_the_order_paid(self):
        body = self.payload()
        with patch(
            'payments.services.verify_payment',
            return_value=paystack_success(5000, currency='NGN'),
        ):
            self.post(body, signature=sign(body))

        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')

    def test_replayed_webhook_notifies_the_buyer_only_once(self):
        body = self.payload()
        signature = sign(body)

        with patch('payments.services.verify_payment', return_value=paystack_success(5000)), \
                patch('payments.views.notify_buyer_payment_success') as notify:
            self.post(body, signature=signature)
            self.post(body, signature=signature)

        self.assertEqual(notify.call_count, 1)

    def test_agent_status_is_not_granted_by_a_webhook(self):
        """item_name is chosen by the buyer, so it must not confer privileges."""
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_user('kojo', 'kojo@example.com', 'pw')
        order = Order.objects.create(
            buyer=user,
            customer_email='kojo@example.com',
            customer_phone='0241234567',
            item_name='Agent Registration Fee',
            quantity=1,
            unit_price=Decimal('1.00'),
        )
        body = json.dumps({
            'event': 'charge.success',
            'data': {'status': 'success', 'reference': order.order_id},
        }).encode()

        with patch('payments.services.verify_payment', return_value=paystack_success(100)):
            self.post(body, signature=sign(body))

        user.refresh_from_db()
        self.assertFalse(user.is_agent)

    def test_unknown_reference_is_accepted_but_changes_nothing(self):
        body = json.dumps({
            'event': 'charge.success',
            'data': {'status': 'success', 'reference': 'KDH-NOTREAL'},
        }).encode()

        response = self.post(body, signature=sign(body))

        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')


@override_settings(PAYSTACK_SECRET_KEY=SECRET)
class InitializePaymentAccessTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        self.user = get_user_model().objects.create_user('kojo', 'kojo@example.com', 'pw')
        self.guest_order = Order.objects.create(
            customer_email='someone@example.com',
            customer_phone='0241234567',
            item_name='1GB MTN',
            quantity=1,
            unit_price=Decimal('6.00'),
        )

    def test_stranger_cannot_reinitialize_someone_elses_order(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('payments:initialize', args=[self.guest_order.order_id])
        )

        self.assertRedirects(response, reverse('home'))
