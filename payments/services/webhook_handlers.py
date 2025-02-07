import logging
from payments.models import PaymentTransaction


logger = logging.getLogger('payments')


class PaymentHandlerService:
    @staticmethod
    def handle_payment_succeeded(payment_id):
        try:
            payment_obj = PaymentTransaction.objects.get(payment_id=payment_id)
            payment_obj.status = 'succeeded'
            payment_obj.save()

            order = payment_obj.order
            order.is_paid = True
            order.status = 'paid'
            order.save()

            logger.info(f"Order {order.order_id} is paid")

        except PaymentTransaction.DoesNotExist:
            raise HandlingOrderNotFoundError(f"Payment {payment_id} not found")

    @staticmethod
    def handle_payment_canceled(payment_id):
        try:
            payment_obj = PaymentTransaction.objects.get(payment_id=payment_id)
            payment_obj.status = 'canceled'
            payment_obj.save()

            order = payment_obj.order
            order.status = 'canceled'
            order.is_paid = False
            order.save()

            logger.info(f"Order {order.order_id} is canceled")

        except PaymentTransaction.DoesNotExist:
            raise HandlingOrderNotFoundError(f"Payment {payment_id} not found")


class HandlingOrderNotFoundError(Exception):
    pass
