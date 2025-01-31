from django.urls import path
from .views import create_payment, payment_webhook


urlpatterns = [
    path('create/<int:order_id>/', create_payment, name='create_payment'),
    path('webhook/', payment_webhook, name='payment_webhook'),
]
