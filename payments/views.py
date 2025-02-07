import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotificationFactory, WebhookNotificationEventType
from yookassa.domain.common import SecurityHelper

from payments.services.utils import get_client_ip
from payments.services.webhook_handlers import PaymentHandlerService, HandlingOrderNotFoundError


logger = logging.getLogger('payments')


@csrf_exempt
def payment_webhook(request):
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
            handler_service.handle_payment_canceled(response_object.id)
        
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

