from random import shuffle

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.utils.html import escape
from django.contrib import messages
from django.views import View

from orders.forms import CreateOrderForm
from orders.models import Order
from orders.services.order_service import create_order_from_cart, EmptyCartError

from payments.models import PaymentTransaction
from payments.services.payment_service import YooKassaPaymentService


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

            if request.headers.get("HX-Request") == "true":
                response = HttpResponse()
                response["HX-Redirect"] = success_url
                return response

            return HttpResponseRedirect(success_url)
            
        except EmptyCartError:
            return HttpResponse("<p>Корзина пустая</p>")
        
        except Exception:
            form.add_error(None, "Произошла внутренняя ошибка. Попробуйте ещё раз или свяжитесь с поддержкой.")
            return render(request, 'orders/order_form.html', {"form": form})
            

class DeliveryDetails(View):
    CITIES = [
        {"id": 1, "name": "Москва", "region": "Центральный округ", "country": "Россия", "population": 12000000, "price": 300},
        {"id": 2, "name": "Санкт-Петербург", "region": "Северо-Западный округ", "country": "Россия", "population": 5000000, "price": 350},
        {"id": 3, "name": "Новосибирск", "region": "Сибирский округ", "country": "Россия", "population": 1600000, "price": 400},
        {"id": 4, "name": "Екатеринбург", "region": "Уральский округ", "country": "Россия", "population": 1500000, "price": 400},
        {"id": 5, "name": "Казань", "region": "Приволжский округ", "country": "Россия", "population": 1300000, "price": 400},
        {"id": 6, "name": "Нижний Новгород", "region": "Приволжский округ", "country": "Россия", "population": 1250000, "price": 400},
        {"id": 7, "name": "Челябинск", "region": "Уральский округ", "country": "Россия", "population": 1200000, "price": 400},
        {"id": 8, "name": "Самара", "region": "Приволжский округ", "country": "Россия", "population": 1150000, "price": 400},
        {"id": 9, "name": "Омск", "region": "Сибирский округ", "country": "Россия", "population": 1150000, "price": 400},
        {"id": 10, "name": "Ростов-на-Дону", "region": "Южный округ", "country": "Россия", "population": 1100000, "price": 400},
        {"id": 11, "name": "Уфа", "region": "Приволжский округ", "country": "Россия", "population": 1100000, "price": 400},
        {"id": 12, "name": "Красноярск", "region": "Сибирский округ", "country": "Россия", "population": 1100000, "price": 400},
        {"id": 13, "name": "Воронеж", "region": "Центральный округ", "country": "Россия", "population": 1080000, "price": 400},
        {"id": 14, "name": "Пермь", "region": "Приволжский округ", "country": "Россия", "population": 1060000, "price": 400},
        {"id": 15, "name": "Волгоград", "region": "Южный округ", "country": "Россия", "population": 1020000, "price": 400},
        {"id": 16, "name": "Краснодар", "region": "Южный округ", "country": "Россия", "population": 950000, "price": 400},
        {"id": 17, "name": "Саратов", "region": "Приволжский округ", "country": "Россия", "population": 840000, "price": 400},
        {"id": 18, "name": "Тюмень", "region": "Уральский округ", "country": "Россия", "population": 780000, "price": 400},
        {"id": 19, "name": "Тольятти", "region": "Приволжский округ", "country": "Россия", "population": 720000, "price": 400},
        {"id": 20, "name": "Ижевск", "region": "Приволжский округ", "country": "Россия", "population": 650000, "price": 400},
        {"id": 21, "name": "Барнаул", "region": "Сибирский округ", "country": "Россия", "population": 650000, "price": 400},
        {"id": 22, "name": "Ульяновск", "region": "Приволжский округ", "country": "Россия", "population": 620000, "price": 400},
        {"id": 23, "name": "Иркутск", "region": "Сибирский округ", "country": "Россия", "population": 620000, "price": 400},
        {"id": 24, "name": "Владивосток", "region": "Дальневосточный округ", "country": "Россия", "population": 610000, "price": 400},
        {"id": 25, "name": "Ярославль", "region": "Центральный округ", "country": "Россия", "population": 600000, "price": 400},
        {"id": 26, "name": "Махачкала", "region": "Северо-Кавказский округ", "country": "Россия", "population": 600000, "price": 400},
        {"id": 27, "name": "Хабаровск", "region": "Дальневосточный округ", "country": "Россия", "population": 580000, "price": 400},
        {"id": 28, "name": "Оренбург", "region": "Приволжский округ", "country": "Россия", "population": 570000, "price": 400},
        {"id": 29, "name": "Новокузнецк", "region": "Сибирский округ", "country": "Россия", "population": 550000, "price": 400},
        {"id": 30, "name": "Кемерово", "region": "Сибирский округ", "country": "Россия", "population": 550000, "price": 400},
        {"id": 31, "name": "Рязань", "region": "Центральный округ", "country": "Россия", "population": 540000, "price": 400},
        {"id": 32, "name": "Тула", "region": "Центральный округ", "country": "Россия", "population": 510000, "price": 400},
        {"id": 33, "name": "Пенза", "region": "Приволжский округ", "country": "Россия", "population": 510000, "price": 400},
        {"id": 34, "name": "Липецк", "region": "Центральный округ", "country": "Россия", "population": 500000, "price": 400},
        {"id": 35, "name": "Чебоксары", "region": "Приволжский округ", "country": "Россия", "population": 490000, "price": 400},
        {"id": 36, "name": "Киров", "region": "Приволжский округ", "country": "Россия", "population": 490000, "price": 400},
        {"id": 37, "name": "Ставрополь", "region": "Северо-Кавказский округ", "country": "Россия", "population": 480000, "price": 400},
        {"id": 38, "name": "Белгород", "region": "Центральный округ", "country": "Россия", "population": 380000, "price": 400},
        {"id": 39, "name": "Архангельск", "region": "Северо-Западный округ", "country": "Россия", "population": 350000, "price": 400},
        {"id": 40, "name": "Вологда", "region": "Северо-Западный округ", "country": "Россия", "population": 310000, "price": 400},
        {"id": 41, "name": "Минск", "region": "", "country": "Беларусь", "population": 2000000, "price": 600},
        {"id": 42, "name": "Гомель", "region": "", "country": "Беларусь", "population": 500000, "price": 600},
        {"id": 43, "name": "Брест", "region": "", "country": "Беларусь", "population": 350000, "price": 600},
        {"id": 44, "name": "Вильнюс", "region": "", "country": "Литва", "population": 580000, "price": 700},
        {"id": 45, "name": "Рига", "region": "", "country": "Латвия", "population": 630000, "price": 700},
        {"id": 46, "name": "Таллин", "region": "", "country": "Эстония", "population": 430000, "price": 700},
        {"id": 47, "name": "Хельсинки", "region": "", "country": "Финляндия", "population": 650000, "price": 800},
        {"id": 48, "name": "Осло", "region": "", "country": "Норвегия", "population": 600000, "price": 800},
        {"id": 49, "name": "Стокгольм", "region": "", "country": "Швеция", "population": 975000, "price": 800},
        {"id": 50, "name": "Копенгаген", "region": "", "country": "Дания", "population": 610000, "price": 800},
    ]


    def get(self, request):
        """Возвращает HTML список подсказок по городам"""
        q = (request.GET.get("city-search") or "").strip().lower()

        if q:
            results = [
                c for c in sorted(self.CITIES, key=lambda x: -x["population"])
                if q in c["name"].lower()
            ][:8]
        else:
            results = sorted(self.CITIES, key=lambda x: -x["population"])[:8]

        if not results:
            return HttpResponse("<p>Город не найден</p>")

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
    