from django.urls import path
from .views import payment_webhook


app_name = 'payments'

urlpatterns = [
    path('webhook/', payment_webhook, name='payment_webhook'),
]
