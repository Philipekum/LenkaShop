from django.shortcuts import render

from goods.models import Products


def catalog(request):
    products = Products.objects.all()

    context = {
        'title': 'Каталог',
        'products': products,
    }
    
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    
    context = {
        'title': product.name,
        'product': product,
    }

    return render(request, 'goods/product.html', context)
