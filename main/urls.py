from django.urls import path

from main.views import index, delivery_info, about_info
from goods.views import catalog


app_name = 'main'

urlpatterns = [
    # path('', index, name='index'),
    path('', catalog, name='index'),
    path('index/', index, name='index'),
    path('delivery-info/', delivery_info, name='delivery_info'),
    path('about-info/', about_info, name='about_info'),
]
