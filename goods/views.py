from django.shortcuts import render

from goods.models import Products


def catalog(request):
    products = Products.objects.all()

    context = {
        'title': 'Каталог',
        'products': products,
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request):
    return render(request, 'goods/product.html')
