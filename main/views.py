from django.shortcuts import render
from goods.models import Collections


def handle_page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)


def index(request):
    collections = Collections.objects.prefetch_related('products').all()

    context = {
        'title': 'Главная страница',
        'collections': collections,
    }

    return render(request, 'main/index.html', context)


def delivery_info(request):
    context = {
        'title': 'Доставка и оплата',
    }
    return render(request, 'main/delivery.html', context)


def about_info(request):
    context = {
        'title': 'О бренде',
    }
    return render(request, 'main/about.html', context)
