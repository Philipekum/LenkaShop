from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

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


class CookieConsentView(View):
    def get(self, request):
        if request.session.get('cookie_consent'):
            return HttpResponse(status=200)
        
        return render(request, 'main/cookie-banner.html')

    def post(self, request):
        request.session['cookie_consent'] = True
        return HttpResponse(status=200)


def reset_cookie(request):
    request.session['cookie_consent'] = False
    return redirect('main:index')
