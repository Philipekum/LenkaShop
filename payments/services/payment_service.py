import uuid
import logging
from typing import Optional

from django.urls import reverse
from django.http import HttpRequest

from yookassa import Payment
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.models.currency import Currency
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

from orders.models import Order
from payments.models import PaymentTransaction


logger = logging.getLogger('payments')


class YooKassaPaymentService:
    @staticmethod
    def create_payment(order: Order, total_price: float, request: HttpRequest) -> Optional[str]:
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

            if payment_response.confirmation is None or payment_response.amount is None:
                return None
            
            logger.info((f"Created payment {payment_response.id}"
                         f"for order {order.order_id}"))

            PaymentTransaction.objects.create(
                order=order,
                payment_id=payment_response.id,
                status=payment_response.status,
                amount=payment_response.amount.value,
            )

            return str(payment_response.confirmation.confirmation_url)

        except Exception as e:
            logger.error(
                f"Error creating payment for order {order.order_id}: {str(e)}")
            return None

    @staticmethod
    def _get_client_ip(request: HttpRequest) -> Optional[str]:
        x_forwarded_for: Optional[str] = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip: str = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
            
        return ip if ip else None
