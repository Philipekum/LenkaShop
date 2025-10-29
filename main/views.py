from django.shortcuts import render
from goods.models import Collections


def handle_page_not_found(request, exception):
    return render(request, 'main/404.html', status=404)


def index(request):
    collections = Collections.objects.all()

    context = {
        'title': 'Главная страница',
        'collections': collections,
    }

    return render(request, 'main/index.html', context)
    