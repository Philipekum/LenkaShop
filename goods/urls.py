from django.urls import path

from goods.views import catalog, product, catalog_load_more


app_name = 'goods'

urlpatterns = [
    path('', catalog, name='index'),
    path('product/<slug:product_slug>/', product, name='product'),
    path('catalog/load_more/', catalog_load_more, name='catalog_load_more'),
]
