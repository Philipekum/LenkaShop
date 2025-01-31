from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages

import yookassa
from dotenv import load_dotenv

import os

from .forms import CreateOrderForm
from .models import Order, OrderItem
from carts.models import Cart
from payments.models import Payment



load_dotenv(override=True)

yookassa.Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
yookassa.Configuration.secret_key = os.getenv('PAYMENT_SECRET_KEY')


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
                with transaction.atomic():
                    session_key = request.session.session_key
                    cart_items = Cart.objects.filter(session_key=session_key)

                    if cart_items.exists():
                        order = Order.objects.create(
                            session_key = session_key,
                            first_name = form.cleaned_data['first_name'],
                            last_name = form.cleaned_data['last_name'],
                            phone_number = form.cleaned_data['phone_number'],
                            email = form.cleaned_data['email'],
                            delivery_address = form.cleaned_data['delivery_address'],
                        )

                        total_price = 0

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.quantity

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()

                            total_price += price * quantity
                        
                        cart_items.delete()

                        payment_data = {
                            "amount": {
                                "value": str(total_price),
                                "currency": "RUB"
                            },
                            "payment_method_data": {
                                "type": "bank_card"
                            },
                            "confirmation": {
                                "type": "redirect",
                                "return_url": request.build_absolute_uri(reverse('orders:success_order', args=[order.order_id]))
                            },
                            "description": f"Оплата заказа #{order.order_id}"
                        }

                        payment = yookassa.Payment.create(payment_data)

                        Payment.objects.create(
                            order_id=order.order_id,
                            payment_id=payment.id,
                            status='pending',
                            amount=total_price
                        )

                        return redirect(payment.confirmation.confirmation_url)
                    
            except ValidationError as e:
                messages.warning(request, str(e))
                
                return redirect('orders:order')
    
    else:
        form = CreateOrderForm()

    context = {
        'title': 'Оформление заказа',
        'form': form,
    }

    return render(request, 'orders/order.html', context=context)
