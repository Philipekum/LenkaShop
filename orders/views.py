from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

from .forms import CreateOrderForm
from .models import Order
from payments.models import PaymentTransaction
from payments.services.create_yookassa_payment import create_yookassa_payment
from orders.services.order_service import create_order_from_cart


def success_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    context = {
        'title': 'Заказ обработан',
        'order_details': [
            ('Номер заказа', order.order_id),
            ('Дата', order.created_timestamp),
            ('ФИО', f'{order.first_name} {order.last_name}'),
            ('EMAIL', order.email),
            ('Номер телефона', order.phone_number),
            ('Статус', order.status),
            ('Доставка', order.delivery_address),
            ('Чек', 'dev'),
        ],
    }
    return render(request, 'orders/success_order.html', context=context)


def order(request):
    if request.method == 'POST':
        form = CreateOrderForm(data=request.POST)
        if form.is_valid():
            try:
                session_key = request.session.session_key

                order_obj, total_price = create_order_from_cart(
                    session_key=session_key,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone_number=form.cleaned_data['phone_number'],
                    email=form.cleaned_data['email'],
                    delivery_address=form.cleaned_data['delivery_address'],
                )

                return_url = request.build_absolute_uri(
                    reverse('orders:success_order', args=[order_obj.order_id])
                )

                payment_response = create_yookassa_payment(
                    order_obj, total_price, return_url
                )

                PaymentTransaction.objects.create(
                    order=order_obj,
                    payment_id=payment_response.id,
                    status='pending',
                    amount=total_price
                )

                return redirect(payment_response.confirmation.confirmation_url)

            except ValueError as ve:
                messages.warning(request, f"Ошибка при оформлении заказа: {ve}")
                return redirect('orders:order')

            except Exception as e:
                messages.warning(request, f"Ошибка при оформлении заказа: {e}")
                return redirect('orders:order')
            
    else:
        form = CreateOrderForm()

        context = {
            'title': 'Оформление заказа',
            'form': form,
        }
        
        return render(request, 'orders/order.html', context=context)
