from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.contrib import messages
from django.views import View

from random import shuffle

from .forms import CreateOrderForm
from .models import Order
from payments.models import PaymentTransaction
from payments.services.create_payment import create_payment
from orders.services.order_service import create_order_from_cart, EmptyCartError


class SuccessOrderView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, order_id=order_id)

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

    def post(self, request, order_id):
        try:
            order = get_object_or_404(Order, order_id=order_id)

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
            
            order_obj, total_price = create_order_from_cart(
                session_key=session_key,
                full_name=form.cleaned_data["full_name"],
                phone_number=form.cleaned_data["phone_number"],
                email=form.cleaned_data["email"],
                delivery_address=form.cleaned_data["delivery_address"],
            )

            success_url = reverse('orders:success_order', args=[order_obj.order_id])

            # payment_response = create_payment(order_obj, total_price, return_url)

            # PaymentTransaction.objects.create(
            #     order=order_obj,
            #     payment_id=payment_response["id"],
            #     status='pending',
            #     amount=total_price
            # )

            # confirmation_url = payment_response["confirmation"]["confirmation_url"]

            if request.headers.get("HX-Request") == "true":
                response = HttpResponse()
                response["HX-Redirect"] = success_url
                return response
            
            return HttpResponseRedirect(success_url)
            
        except EmptyCartError:
            return HttpResponse("<p>Корзина пустая</p>")

        except Exception as e:
            form.add_error(None, f"Произошла внутренняя ошибка. Попробуйте ещё раз или свяжитесь с поддержкой. {e}")
            return render(request, 'orders/order_form.html', {"form": form})
            

class DeliveryDetails(View):
    CITIES = [
        {"id": 1, "name": "Москва", "region": "Центральный округ", "country": "Россия", "population": 12000000, "price": 300},
        {"id": 2, "name": "Санкт-Петербург", "region": "Северо-Западный округ", "country": "Россия", "population": 5000000, "price": 350},
        {"id": 3, "name": "Казань", "region": "Приволжский округ", "country": "Россия", "population": 1300000, "price": 400},
        {"id": 4, "name": "Минск", "region": "", "country": "Беларусь", "population": 2000000, "price": 600},
        {"id": 5, "name": "Хельсинки", "region": "", "country": "Финляндия", "population": 650000, "price": 800},
    ]

    def get(self, request):
        """Возвращает HTML список подсказок по городам"""
        q = (request.GET.get("city-search") or "").strip().lower()

        # Если пусто — показываем все города (до 8)
        if q:
            results = [
                c for c in sorted(self.CITIES, key=lambda x: -x["population"])
                if q in c["name"].lower()
            ][:8]
        else:
            results = sorted(self.CITIES, key=lambda x: -x["population"])[:8]

        if not results:
            return HttpResponse("<p>Ничего не найдено</p>")

        html = "<ul class='city-suggestions'>"
        for c in results:
            label = f"{escape(c['country']+', ' if c['country']!='Россия' else '')}{escape(c['region'])}, {escape(c['name'])}"
            html += f"""
                <li>
                    <button 
                        type='button'
                        hx-post='/new-site/order/delivery/'
                        hx-vals='{{"city_id": "{c["id"]}"}}'
                        hx-target='#delivery-price'
                        hx-swap='innerHTML'
                    >{label}</button>
                </li>
            """
        html += "</ul>"
        return HttpResponse(html)


    def post(self, request):
        """Возвращает цену доставки по выбранному городу"""
        city_id = request.POST.get("city_id")
        try:
            city = next(c for c in self.CITIES if str(c["id"]) == city_id)
        except StopIteration:
            return HttpResponse("<p>Ошибка: город не найден</p>")

        html = f"<p>Стоимость доставки в {escape(city['name'])}: <b>{city['price']} ₽</b></p>"
        return HttpResponse(html)
    