from django.urls import path
from django.shortcuts import redirect

from orders.views import OrderView, SuccessOrderView


app_name = 'orders'


def test_paid_success_order(request):
    return redirect('orders:success_order', order_id=745217511)


def test_unpaid_success_order(request):
    return redirect('orders:success_order', order_id=736432925)


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('success_order/<int:order_id>/', SuccessOrderView.as_view(),
         name='success_order'),
    path('success_order/paid', test_paid_success_order,
         name='success_order_test_1'),
    path('success_order/unpaid', test_unpaid_success_order,
         name='success_order_test_2'),
]
