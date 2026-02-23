import logging

from django.http import HttpResponse
from django.views import View
from django.utils.html import escape


logger = logging.getLogger("delivery")


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
    NOT_FOUND_CITY = "Город не найден"
    ERROR_NOT_FOUND_CITY = "Ошибка: город не найден"

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
            logger.warning(self.NOT_FOUND_CITY)
            return HttpResponse(f"<p>{self.NOT_FOUND_CITY}</p>")

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
            logger.error(self.ERROR_NOT_FOUND_CITY)
            return HttpResponse(f"<p>{self.ERROR_NOT_FOUND_CITY}</p>")

        html = f"<p>Стоимость доставки в {escape(city['name'])}: <b>{city['price']} ₽</b></p>"
        return HttpResponse(html)
