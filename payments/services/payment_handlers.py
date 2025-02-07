import json
import logging

from django.http import HttpResponse
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper

from .utils import get_client_ip
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
    def handle_payment_canceled(payment_id, cancel_reason=None):
        try:
            payment_obj = PaymentTransaction.objects.get(payment_id=payment_id)
            payment_obj.status = 'canceled'
            payment_obj.save()

            order = payment_obj.order
            order.status = 'canceled'
            order.save()

            logger.info(f"Order {order.order_id} canceled due to {cancel_reason}.")

        except PaymentTransaction.DoesNotExist:
            raise HandlingOrderNotFoundError(f"Payment {payment_id} not found")


class HandlingOrderNotFoundError(Exception):
    pass


def handle_payment(request):
    ip = get_client_ip(request)  

    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse("Unauthorized IP", status=401)

    try:
        event_json = json.loads(request.body)
    except json.JSONDecodeError:
        logger.error('Invalid JSON recieved')
        return HttpResponse("Invalid JSON", status=400)

    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object

        handler_service = PaymentHandlerService()

        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            handler_service.handle_payment_succeeded(response_object.id)

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            cancel_reason = response_object.cancellation_details.reason
            handler_service.handle_payment_canceled(response_object.id, cancel_reason)
        
        else:
            logger.error(f'Unsupported event type: {notification_object.event}')
            return HttpResponse("Unsupported event type", status=403)  

        return HttpResponse("Success", status=200)  
    
    except HandlingOrderNotFoundError as e:
        logger.error(f'{e}')
        return HttpResponse("Order not found", status=404)

    except Exception as e:
        logger.error(f'Unexpected error: {e}')
        return HttpResponse("Server error", status=500)
