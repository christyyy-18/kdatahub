from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from .catalog import get_price
from .models import Order

User = get_user_model()

VALID_FORM = {
    'customer_name': 'Ama Mensah',
    'customer_email': 'ama@example.com',
    'customer_phone': '0241234567',
    'quantity': 1,
}


def fake_paystack_init(order, email):
    return {
        'status': True,
        'data': {
            'reference': order.order_id,
            'authorization_url': 'https://checkout.paystack.com/fake',
        },
    }


@patch('orders.views.notify_manager_new_order', lambda *a, **k: None)
@patch('orders.views.notify_buyer_order_placed', lambda *a, **k: None)
@patch('orders.views.initialize_payment', fake_paystack_init)
class CreateOrderPricingTests(TestCase):
    def setUp(self):
        cache.clear()

    def post_order(self, **overrides):
        data = dict(VALID_FORM)
        data.update(overrides)
        return self.client.post(reverse('orders:create_order'), data)

    def test_posted_unit_price_is_ignored(self):
        """A buyer cannot name their own price by editing the form."""
        self.post_order(item_name='100GB MTN', unit_price='0.01')

        order = Order.objects.get()
        self.assertEqual(order.unit_price, Decimal('420.00'))
        self.assertEqual(order.total_amount, Decimal('420.00'))

    def test_unknown_package_is_rejected(self):
        response = self.post_order(item_name='999GB MTN', unit_price='1.00')

        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, 'choose a data package')

    def test_quantity_above_the_cap_is_rejected(self):
        response = self.post_order(item_name='1GB MTN', quantity=5000)

        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, 'Quantity must be between')

    def test_invalid_phone_is_rejected_before_sms_is_sent(self):
        response = self.post_order(item_name='1GB MTN', customer_phone='12')

        self.assertEqual(Order.objects.count(), 0)
        self.assertContains(response, 'valid Ghana phone number')

    def test_total_follows_quantity(self):
        self.post_order(item_name='10GB MTN', quantity=3)

        order = Order.objects.get()
        self.assertEqual(order.total_amount, Decimal('150.00'))

    def test_agent_gets_the_discounted_price(self):
        agent = User.objects.create_user('agent', 'agent@example.com', 'pw')
        agent.is_agent = True
        agent.save()
        self.client.force_login(agent)

        self.post_order(item_name='10GB MTN')

        order = Order.objects.get()
        self.assertEqual(order.unit_price, Decimal('45.00'))

    def test_repeated_orders_are_throttled(self):
        for _ in range(5):
            self.post_order(item_name='1GB MTN')
        response = self.post_order(item_name='1GB MTN')

        self.assertEqual(Order.objects.count(), 5)
        self.assertContains(response, 'Too many orders')


class PackagePrefillTests(TestCase):
    def test_package_query_param_preselects_the_option(self):
        response = self.client.get(reverse('orders:create_order'), {'package': '10GB MTN'})

        self.assertContains(response, 'value="10GB MTN" class="mtn" selected')
        self.assertEqual(response.context['selected_price'], Decimal('50.00'))

    def test_unknown_package_query_param_is_ignored(self):
        response = self.client.get(reverse('orders:create_order'), {'package': 'free stuff'})

        self.assertIsNone(response.context['selected_key'])
        self.assertEqual(response.status_code, 200)

    def test_home_links_every_package_to_the_order_form(self):
        response = self.client.get(reverse('home'))

        self.assertContains(response, 'href="/orders/create/?package=10GB%20MTN"')
        self.assertContains(response, 'href="/orders/create/?package=5GB%20Telecel"')


class CatalogTests(TestCase):
    def test_agent_price_is_ten_percent_off(self):
        self.assertEqual(get_price('1GB MTN'), Decimal('6.00'))
        self.assertEqual(get_price('1GB MTN', is_agent=True), Decimal('5.40'))

    def test_unknown_package_has_no_price(self):
        self.assertIsNone(get_price('1TB MTN'))


class OrderAccessTests(TestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user('kojo', 'kojo@example.com', 'pw')
        self.guest_order = Order.objects.create(
            customer_name='Someone Else',
            customer_email='someone@example.com',
            customer_phone='0209876543',
            item_name='1GB MTN',
            quantity=1,
            unit_price=Decimal('6.00'),
        )

    def test_logged_in_user_cannot_read_a_guest_order(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('orders:order_detail', args=[self.guest_order.order_id])
        )

        self.assertRedirects(response, reverse('orders:my_orders'))

    def test_logged_in_user_cannot_download_a_guest_invoice(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse('orders:invoice', args=[self.guest_order.order_id])
        )

        self.assertEqual(response.status_code, 302)

    def test_manager_can_read_a_guest_order(self):
        manager = User.objects.create_user('boss', 'boss@example.com', 'pw')
        manager.is_manager = True
        manager.save()
        self.client.force_login(manager)

        response = self.client.get(
            reverse('orders:order_detail', args=[self.guest_order.order_id])
        )

        self.assertEqual(response.status_code, 200)

    def test_manager_csv_export_survives_guest_orders(self):
        manager = User.objects.create_user('boss', 'boss@example.com', 'pw')
        manager.is_manager = True
        manager.save()
        self.client.force_login(manager)

        response = self.client.get(reverse('orders:export_orders'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Someone Else', response.content.decode())


class TrackOrderTests(TestCase):
    def setUp(self):
        cache.clear()
        self.order = Order.objects.create(
            customer_name='Ama Mensah',
            customer_email='ama@example.com',
            customer_phone='0241234567',
            item_name='1GB MTN',
            quantity=1,
            unit_price=Decimal('6.00'),
        )

    def test_stranger_sees_masked_contact_details(self):
        response = self.client.get(
            reverse('orders:track_order'), {'ticket_id': self.order.order_id}
        )
        body = response.content.decode()

        self.assertIn(self.order.order_id, body)
        self.assertNotIn('ama@example.com', body)
        self.assertNotIn('0241234567', body)
        self.assertIn('a***a@example.com', body)

    def test_owner_sees_full_contact_details(self):
        owner = User.objects.create_user('ama', 'ama@example.com', 'pw')
        self.order.buyer = owner
        self.order.save()
        self.client.force_login(owner)

        response = self.client.get(
            reverse('orders:track_order'), {'ticket_id': self.order.order_id}
        )

        self.assertContains(response, 'ama@example.com')

    def test_lookups_are_throttled(self):
        for _ in range(15):
            self.client.get(reverse('orders:track_order'), {'ticket_id': self.order.order_id})

        response = self.client.get(
            reverse('orders:track_order'), {'ticket_id': self.order.order_id}
        )

        self.assertContains(response, 'Too many lookups')
