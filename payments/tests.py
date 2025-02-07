from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from payments.models import PaymentTransaction
from orders.models import Order
import json


class PaymentWebhookTestCase(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            order_id=123456,
            first_name="Test",
            last_name="User",
            is_paid=False,
            status="pending"
        )

        self.payment = PaymentTransaction.objects.create(
            order=self.order,
            payment_id="test_payment_id_123",
            status="pending",
            amount=1000.00
        )

        self.url = reverse("payments:payment_webhook") 

    @patch("payments.services.payment_handlers.SecurityHelper.is_ip_trusted")
    def test_payment_succeeded(self, mock_ip_check):
        mock_ip_check.return_value = True

        webhook_data = {
            "type": "notification",
            "event": "payment.succeeded",
            "object": {
                "id": "test_payment_id_123"
            }
        }

        response = self.client.post(
            self.url,
            data=json.dumps(webhook_data),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

        payment = PaymentTransaction.objects.get(payment_id="test_payment_id_123")
        self.assertEqual(payment.status, "succeeded")

        order = payment.order
        self.assertTrue(order.is_paid)
        self.assertEqual(order.status, "paid")

    # @patch("payments.services.payment_handlers.SecurityHelper.is_ip_trusted")
    # def test_payment_canceled(self, mock_ip_check):
    #     mock_ip_check.return_value = True

    #     webhook_data = {
    #         "type": "notification",
    #         "event": "payment.canceled",
    #         "object": {
    #             "id": "test_payment_id_123",
    #             "cancellation_details": {
    #                 "reason": "user_declined"
    #             }
    #         }
    #     }

    #     response = self.client.post(
    #         self.url,
    #         data=json.dumps(webhook_data),
    #         content_type="application/json"
    #     )

    #     self.assertEqual(response.status_code, 200)

    #     payment = PaymentTransaction.objects.get(payment_id="test_payment_id_123")
    #     self.assertEqual(payment.status, "canceled")

    #     order = payment.order
    #     self.assertEqual(order.status, "canceled")

    # def test_invalid_json(self):
    #     response = self.client.post(
    #         self.url,
    #         data="INVALID_JSON",
    #         content_type="application/json"
    #     )

    #     self.assertEqual(response.status_code, 400)

    # @patch("payments.services.payment_handlers.SecurityHelper.is_ip_trusted")
    # def test_untrusted_ip(self, mock_ip_check):
    #     mock_ip_check.return_value = False

    #     webhook_data = {
    #         "type": "notification",
    #         "event": "payment.succeeded",
    #         "object": {
    #             "id": "test_payment_id_123"
    #         }
    #     }

    #     response = self.client.post(
    #         self.url,
    #         data=json.dumps(webhook_data),
    #         content_type="application/json"
    #     )

    #     self.assertEqual(response.status_code, 401)
