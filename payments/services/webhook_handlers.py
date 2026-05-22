import logging
from django.db import transaction
from django.http import HttpRequest
from yookassa.domain.notification import WebhookNotification
from payments.models import PaymentTransaction


logger = logging.getLogger('payments')


class PaymentHandlerService:
    @staticmethod
    def parse_webhook_notification(request: HttpRequest) -> WebhookNotification:
        try:
            request_body = request.body
            return WebhookNotification(request_body)
        except Exception as e:
            logger.error(f"Error parsing webhook: {str(e)}")
            raise

    @staticmethod
    @transaction.atomic
    def handle_payment_succeeded(payment_id: int) -> None:
        try:
            payment_obj = PaymentTransaction.objects.select_for_update().get(
                payment_id=payment_id
            )

            payment_obj.status = 'succeeded'
            payment_obj.save()

            order = payment_obj.order
            order.status = 'paid'
            order.save()

            logger.info(f"Order {order.order_id} successfully paid")

        except PaymentTransaction.DoesNotExist:
            message = f"Payment {payment_id} not found"
            logger.error(message)
            raise HandlingOrderNotFoundError(message)

    @staticmethod
    @transaction.atomic  
    def handle_payment_canceled(payment_id: int) -> None:
        try:
            payment_obj = PaymentTransaction.objects.select_for_update().get(
                payment_id=payment_id
            )

            payment_obj.status = 'canceled'
            payment_obj.save()

            order = payment_obj.order
            order.status = 'canceled'
            order.save()

            logger.info(f"Order {order.order_id} payment canceled")

        except PaymentTransaction.DoesNotExist:
            message = f"Payment {payment_id} not found"
            logger.error(message)
            raise HandlingOrderNotFoundError(message)


class HandlingOrderNotFoundError(Exception):
    pass
