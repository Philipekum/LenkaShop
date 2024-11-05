from django.urls import path
from carts.views import *


app_name = 'carts'

urlpatterns = [
    path('cart_add/', CartAddView.as_view(), name='cart_add'),
    path('cart_remove/', CartRemoveView.as_view(), name='cart_remove'),
    # path('cart_change/', cart_change, name='cart_change'),
]
