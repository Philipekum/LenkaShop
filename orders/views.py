import random

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.views import View

from goods.models import Products
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem
from orders.services.order_service import (create_order_from_cart,
                                           EmptyCartError)
from payments.models import PaymentTransaction
from payments.services.payment_service import YooKassaPaymentService


class SuccessOrderView(View):
    def get(self, request, order_id):
        order = get_object_or_404(
            Order.objects.select_related('delivery_service'),
            order_id=order_id
        )

        order_items = OrderItem.objects.filter(order=order)\
            .select_related('product')\
            .only('product', 'quantity')

        product_ids = [item.product.id for item in order_items if item.product]
        similar_products_qs = (Products.objects.filter(
            similar_to_this__id__in=product_ids
        ).distinct()
         .select_related('flag')
         .prefetch_related('images'))

        similar_products = list(similar_products_qs)

        if len(similar_products) < 5:
            needed = 5 - len(similar_products)
            exclude_ids = [p.id for p in similar_products] + product_ids

            random_products = (Products.objects
                               .exclude(id__in=exclude_ids)
                               .select_related('flag')
                               .prefetch_related('images')
                               .order_by('?')[:needed * 2])

            similar_products.extend(random_products)

        similar_products = similar_products[:5]
        random.shuffle(similar_products)

        context = {
            'title': order.get_status_display(),
            'order': order,
            'order_items': order_items,
            'similar_products': similar_products,
            'total_price': order.orderitem_set.total_price(),
        }

        return render(request, 'orders/success_order.html', context=context)

    def post(self, request, order_id):
        try:
            order = get_object_or_404(Order, order_id=order_id)
            total_price = order.orderitem_set.total_price()

            payment_data = YooKassaPaymentService.create_payment(
                order, total_price, request
            )

            PaymentTransaction.objects.create(
                order=order,
                payment_id=payment_data['id'],
                status=payment_data['status'],
                amount=total_price
            )

            return JsonResponse({
                'redirect_url': payment_data['confirmation_url']
            })

        except Exception:
            # logger.error(f"Payment creation error: {str(e)}")
            messages.error(request,
                           'Ошибка при создании платежа. Попробуйте еще раз!')
            return redirect(reverse('orders:success_order',
                                    args=[order.order_id]))


class OrderView(View):
    def get(self, request):
        form = CreateOrderForm()

        context = {
            'title': 'Оформление заказа',
            'form': form,
        }

        return render(request, 'orders/order.html', context=context)

    def post(self, request):
        form = CreateOrderForm(data=request.POST)

        if not form.is_valid():
            return render(request, 'orders/order_form.html', {"form": form})

        try:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            order_obj, _ = create_order_from_cart(
                session_key=session_key,
                full_name=form.cleaned_data["full_name"],
                phone_number=form.cleaned_data["phone_number"],
                email=form.cleaned_data["email"],
                delivery_address=form.cleaned_data["delivery_address"],
            )

            success_url = reverse('orders:success_order',
                                  args=[order_obj.order_id])

            if request.headers.get("HX-Request") == "true":
                response = HttpResponse()
                response["HX-Redirect"] = success_url
                return response

            return HttpResponseRedirect(success_url)

        except EmptyCartError:
            return HttpResponse("<p>Корзина пустая</p>")

        except Exception:
            form.add_error(None,
                           ("Произошла внутренняя ошибка. "
                            "Попробуйте ещё раз или свяжитесь с поддержкой."))
            return render(request, 'orders/order_form.html', {"form": form})
