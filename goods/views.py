from django.shortcuts import render
from django.core.paginator import Paginator

from goods.models import Products


def catalog(request):
    page = int(request.GET.get('page', 1))

    products = Products.objects.all()

    paginator = Paginator(products, 7)
    current_page = paginator.page(page)

    context = {
        'title': 'Каталог',
        'products': current_page,
    }
    
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    
    context = {
        'title': product.name,
        'product': product,
    }

    return render(request, 'goods/product.html', context)
