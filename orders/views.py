from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from carts.models import Cart
from .forms import CreateOrderForm
from .models import Order, OrderItem
from payments.models import PaymentTransaction
from payments.services.create_yookassa_payment import create_yookassa_payment


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
                            session_key=session_key,
                            first_name=form.cleaned_data['first_name'],
                            last_name=form.cleaned_data['last_name'],
                            phone_number=form.cleaned_data['phone_number'],
                            email=form.cleaned_data['email'],
                            delivery_address=form.cleaned_data['delivery_address'],
                        )

                        total_price = 0

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = product.name
                            price = product.sell_price()
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

                        return_url = request.build_absolute_uri(
                            reverse('orders:success_order', args=[order.order_id])
                        )

                        payment_response = create_yookassa_payment(order, total_price, return_url)

                        PaymentTransaction.objects.create(
                            order=order,
                            payment_id=payment_response.id,
                            status='pending',
                            amount=total_price
                        )

                        return redirect(payment_response.confirmation.confirmation_url)
                    
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
