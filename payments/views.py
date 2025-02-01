import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotificationFactory
from payments.models import PaymentTransaction


@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponse(status=400)

        notification = WebhookNotificationFactory().create(body)

        if notification.event == "payment.succeeded":
            payment_id = notification.object.id
            try:
                payment_obj = PaymentTransaction.objects.get(payment_id=payment_id)
                payment_obj.status = 'succeeded'
                payment_obj.save()

                order = payment_obj.order
                order.is_paid = True
                order.status = 'paid'
                order.save()

            except PaymentTransaction.DoesNotExist:
                return HttpResponse(status=404)

        elif notification.event == "payment.canceled":
            payment_id = notification.object.id
            try:
                payment_obj = PaymentTransaction.objects.get(payment_id=payment_id)
                payment_obj.status = 'canceled'
                payment_obj.save()

                order = payment_obj.order
                order.status = 'canceled'
                order.save()

            except PaymentTransaction.DoesNotExist:
                return HttpResponse(status=404)

        return HttpResponse(status=200)
    
    return HttpResponse(status=405)
