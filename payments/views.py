from django.http import JsonResponse, Http404
from yookassa import Configuration, Payment
from dotenv import load_dotenv
import os
from django.conf import settings
from orders.models import Order 
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from yookassa.domain.notification import WebhookNotificationFactory
from .models import Payment


load_dotenv(override=True)

Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
Configuration.secret_key = os.getenv('PAYMENT_SECRET_KEY')


def create_payment(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)

        payment_data = {
            "amount": {
                "value": str(order.total_price),  
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://ваш-домен.рф/success/" 
            },
            "description": f"Order #{order_id}"
        }

        payment = Payment.create(payment_data)

        Payment.objects.create(
            order_id=order_id,
            payment_id=payment.id,
            status=payment.status,
            amount=order.total_price
        )

        return JsonResponse({"payment_url": payment.confirmation.confirmation_url})
    
    except Order.DoesNotExist:
        raise Http404("Заказ не найден")


@csrf_exempt
def payment_webhook(request):
    if request.method == "POST":
        body = json.loads(request.body)
        notification = WebhookNotificationFactory().create(body)

        if notification.event == "payment.succeeded":
            payment_id = notification.object.id
            try:
                payment = Payment.objects.get(payment_id=payment_id)
                payment.status = 'succeeded'
                payment.save()

                # Обновляем статус заказа
                order = Order.objects.get(id=payment.order_id)
                order.payment_status = 'Оплачен'
                order.save()

            except (Payment.DoesNotExist, Order.DoesNotExist):
                pass  # Можно добавить логирование ошибки

        elif notification.event == "payment.canceled":
            payment_id = notification.object.id
            try:
                payment = Payment.objects.get(payment_id=payment_id)
                payment.status = 'canceled'
                payment.save()

                # Обновляем статус заказа
                order = Order.objects.get(id=payment.order_id)
                order.payment_status = 'Отменен'
                order.save()

            except (Payment.DoesNotExist, Order.DoesNotExist):
                pass

        return HttpResponse(status=200)
    
    return HttpResponse(status=405)
