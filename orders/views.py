from django.shortcuts import render, redirect
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages

from .forms import CreateOrderForm
from .models import Order, OrderItem
from carts.models import Cart


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

                        for cart_item in cart_items:
                            product = cart_item.product
                            name = cart_item.product.name
                            price = cart_item.product.sell_price()
                            quantity = cart_item.product.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f'Недостаточное количество товара {product.name}: запрашивается - {quantity}, в наличии - {product.quantity}')

                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()
                        
                        cart_items.delete()

                        messages.success(request, 'Заказ оформлен!')

                        return redirect('main:index')
                    
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
