import logging
from django.db import transaction
from yookassa.domain.notification import WebhookNotification
from payments.models import PaymentTransaction


logger = logging.getLogger('payments')


class PaymentHandlerService:
    @staticmethod
    def parse_webhook_notification(request_body):
        try:
            return WebhookNotification(request_body)
        except Exception as e:
            logger.error(f"Error parsing webhook: {str(e)}")
            raise
    
    @staticmethod
    @transaction.atomic
    def handle_payment_succeeded(payment_id, payment_data=None):
        try:
            payment_obj = PaymentTransaction.objects.select_for_update().get(
                payment_id=payment_id
            )
            
            payment_obj.status = 'succeeded'
            payment_obj.save()
            
            order = payment_obj.order
            order.is_paid = True
            order.status = 'paid'
            order.save()
            
            PaymentHandlerService._send_payment_success_notifications(order, payment_obj)
            
            logger.info(f"Order {order.order_id} successfully paid")

        except PaymentTransaction.DoesNotExist:
            raise HandlingOrderNotFoundError(f"Payment {payment_id} not found")

    @staticmethod
    @transaction.atomic  
    def handle_payment_canceled(payment_id, payment_data=None):
        try:
            payment_obj = PaymentTransaction.objects.select_for_update().get(
                payment_id=payment_id
            )
            
            payment_obj.status = 'canceled'
            payment_obj.save()
            
            order = payment_obj.order
            order.status = 'canceled'
            order.is_paid = False
            order.save()
            
            logger.info(f"Order {order.order_id} payment canceled")

        except PaymentTransaction.DoesNotExist:
            raise HandlingOrderNotFoundError(f"Payment {payment_id} not found") 

    @staticmethod
    def _send_payment_success_notifications(order, payment):
        # TODO: Реализовать отправку email
        pass


class HandlingOrderNotFoundError(Exception):
    pass
