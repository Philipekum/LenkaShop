from django.urls import path
from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('', order, name='order'),
    path('success_order/<uuid:order_id>/', success_order, name='success_order'),
]
