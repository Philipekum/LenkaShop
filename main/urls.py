from django.urls import path

from main.views import index, delivery_info, about_info, CookieConsentView, reset_cookie
from goods.views import catalog
from app import settings


app_name = 'main'

urlpatterns = [
    # path('', index, name='index'),
    path('', catalog, name='index'),
    path('index/', index, name='index'),
    path('delivery-info/', delivery_info, name='delivery_info'),
    path('about-info/', about_info, name='about_info'),
    path('cookie-consent/', CookieConsentView.as_view(), name='cookie_consent'),
]

if settings.DEBUG:
    urlpatterns += [
        path('reset-cookie/', reset_cookie, name='reset_cookie'),
    ]
