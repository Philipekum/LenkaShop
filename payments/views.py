import logging
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from payments.services.utils import get_client_ip, validate_ip
from payments.services.webhook_handlers import (
    PaymentHandlerService,
    HandlingOrderNotFoundError
)


logger = logging.getLogger('payments')


@csrf_exempt
def payment_webhook(request):
    if not settings.DEBUG:
        ip = get_client_ip(request)
        if not validate_ip(ip, settings.YOOKASSA_ALLOWED_IPS):
            logger.warning(f"Unauthorized IP attempt: {ip}")
            return HttpResponse("Unauthorized IP", status=401)

    try:
        notification = PaymentHandlerService.parse_webhook_notification(
            request.body)

        if notification.event == 'payment.succeeded':
            payment_id = notification.object.id
            PaymentHandlerService.handle_payment_succeeded(
                payment_id,
                payment_data=notification.object
            )

        elif notification.event == 'payment.canceled':
            payment_id = notification.object.id
            PaymentHandlerService.handle_payment_canceled(
                payment_id,
                payment_data=notification.object
            )

        else:
            logger.info(f'Unhandled event type: {notification.event}')
            return HttpResponse("Event not handled", status=200)

        return HttpResponse("Success", status=200)

    except HandlingOrderNotFoundError as e:
        logger.error(f'Order not found: {e}')
        return HttpResponse("Order not found", status=404)

    except Exception as e:
        logger.error(f'Webhook processing error: {e}')
        return HttpResponse("Server error", status=500)
