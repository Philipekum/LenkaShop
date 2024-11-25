from django.urls import path
from orders.views import *


app_name = 'orders'

urlpatterns = [
    path('', order, name='order'),
]
