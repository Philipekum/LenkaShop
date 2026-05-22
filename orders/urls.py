from django.urls import path
from orders.views import OrderView, SuccessOrderView


app_name = 'orders'


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('success_order/<int:order_id>/', SuccessOrderView.as_view(),
         name='success_order'),
]
