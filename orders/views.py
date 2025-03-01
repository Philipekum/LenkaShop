from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponseNotFound
from django.contrib import messages

from random import shuffle

from .forms import CreateOrderForm
from .models import Order
from payments.models import PaymentTransaction
from payments.services.create_payment import create_payment
from orders.services.order_service import create_order_from_cart, EmptyCartError


def success_order(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)

    if request.method == 'POST':
        try:
            total_price = order.orderitem_set.total_price()

            return_url = request.build_absolute_uri(
                reverse('orders:success_order', args=[order.order_id])
            )

            payment_response = create_payment(
                order, total_price, return_url
            )

            if payment_response is None:
                raise ConnectionError

            confirmation_url = payment_response['confirmation']['confirmation_url']

            return JsonResponse({
                'redirect_url': confirmation_url
            })
        
        except Exception as e:
            messages.error(request, 'Ошибка при создании платежа. Попробуйте еще раз!')
            return redirect(reverse('orders:success_order', args=[order.order_id]))

    else:
        order_items = order.orderitem_set.all()

        total_price = order.orderitem_set.total_price()
        
        similar_products = []

        for item in order_items:
            for prod in item.product.similar_products.all():
                if prod not in similar_products:
                    similar_products.append(prod)
        
        shuffle(similar_products)

        title = 'Спасибо за покупку!' if order.is_paid else 'Заказ ждет оплаты'
            
        context = {
            'title': title,
            'order': order,
            'order_items': order_items,
            'similar_products': similar_products[:3],
            'total_price': total_price,
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

                payment_response = create_payment(
                    order_obj, total_price, return_url
                )

                if payment_response is None:
                    messages.error(request, 'Ошибка при создании платежа. Попробуйте еще раз!')

                    return render(request, 'orders/order.html', {'title': 'Оформление заказа', 'form': form})

                
                confirmation_url = payment_response['confirmation']['confirmation_url']

                PaymentTransaction.objects.create(
                    order=order_obj,
                    payment_id=payment_response["id"],
                    status='pending',
                    amount=total_price
                )

                return redirect(confirmation_url)
            
            except EmptyCartError:
                messages.error(request, 'Корзина пустая')

            except Exception as e:
                messages.error(request, 'Произошла ошибка при оформлении заказа. Попробуйте снова!')
            
        else:
            for _, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")

    else:
        form = CreateOrderForm()

    context = {
        'title': 'Оформление заказа',
        'form': form,
    }
        
    return render(request, 'orders/order.html', context=context)
