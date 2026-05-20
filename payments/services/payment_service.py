import uuid
import logging
from django.urls import reverse

from orders.models import Order
from yookassa import Payment
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models.currency import Currency
from yookassa.domain.request.payment_request_builder import (
    PaymentRequestBuilder)


logger = logging.getLogger('payments')


class YooKassaPaymentService:
    @staticmethod
    def create_payment(order: Order, total_price, request):
        try:
            return_url = request.build_absolute_uri(
                reverse('orders:success_order', args=[order.order_id])
            )

            builder = PaymentRequestBuilder()
            builder.set_amount({"value": f"{total_price:.2f}",
                                "currency": Currency.RUB}) \
                .set_confirmation({
                    "type": ConfirmationType.REDIRECT, 
                    "return_url": return_url
                }) \
                .set_capture(True) \
                .set_description(f"Оплата заказа #{order.order_id}") \
                .set_metadata({"order_id": str(order.order_id)})

            request_obj = builder.build()

            client_ip = YooKassaPaymentService._get_client_ip(request)
            if client_ip:
                request_obj.client_ip = client_ip

            idempotence_key = str(uuid.uuid4())

            payment_response = Payment.create(request_obj, idempotence_key)

            logger.info((f"Created payment {payment_response.id}"
                         f"for order {order.order_id}"))

            if payment_response.confirmation is None:
                raise ValueError()

            if payment_response.amount is None:
                raise ValueError()
            
            response = {
                'id': payment_response.id,
                'status': payment_response.status,
                'confirmation_url': (
                    payment_response.confirmation.confirmation_url),
                'amount': payment_response.amount.value,
            }
        
            return response

        except Exception as e:
            logger.error(
                f"Error creating payment for order {order.order_id}: {str(e)}")
            raise

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
