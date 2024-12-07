from django.shortcuts import render, get_object_or_404

from goods.models import Products, Categories


def catalog(request):
    category_slug = request.GET.get('category')
    products = Products.objects.all()

    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        products = products.filter(category=category)
    
    else:
        category = None
    
    categories = Categories.objects.all()

    context = {
        'title': 'Каталог',
        'products': products,
        'categories': categories,
        'selected_category': category,
    }
    
    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)
    
    context = {
        'title': product.name,
        'product': product,
    }

    return render(request, 'goods/product.html', context)
