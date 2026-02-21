from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponse

from goods.models import Products, Categories, Collections


BLOCK_LIMIT = 6


def catalog(request):
    category_slug = request.GET.get('category')

    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        products = (Products.objects.filter(category=category)
                    .select_related('flag').prefetch_related('images'))
    else:
        category = None
        products = (Products.objects
                    .select_related('flag').prefetch_related('images').all())

    categories = Categories.objects.all()
    offset = 0

    context = {
        'title': 'Каталог',
        'products': products[:BLOCK_LIMIT],
        'categories': categories,
        'selected_category': category,
        'has_more': len(products) > BLOCK_LIMIT,
        'limit': BLOCK_LIMIT,
        'offset': offset + BLOCK_LIMIT, 
    }

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):
    product = Products.objects.get(slug=product_slug)

    context = {
        'title': product.name,
        'product': product,
    }

    return render(request, 'goods/product.html', context)


def collection(request, collection_slug):
    collection = get_object_or_404(Collections, slug=collection_slug)
    collection_products = (collection.products.select_related('flag')
                           .prefetch_related('images').all())
    context = {
        'title': collection.name,
        'collection': collection,
        'collection_products': collection_products,
    }

    return render(request, 'goods/collection.html', context)


def catalog_load_more(request):
    category_slug = request.GET.get('category')
    offset = int(request.GET.get('offset', 0))

    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        products_qs = (Products.objects.filter(category=category)
                       .select_related('flag').prefetch_related('images'))

    else:
        products_qs = (Products.objects
                       .select_related('flag')
                       .prefetch_related('images').all())

    products = products_qs[offset:offset + BLOCK_LIMIT]

    total_count = products_qs.count()
    has_more = total_count > offset + BLOCK_LIMIT

    html_products = render_to_string('goods/includes/catalog_items.html',
                                     {'products': products})
    html_button = ''

    if has_more:
        html_button = render_to_string('goods/includes/load_more_button.html',
                                       {
                                            'offset': offset + BLOCK_LIMIT,
                                            'category_slug': category_slug
                                        })

    else:
        html_button = '<div id="load-more-button" hx-swap-oob="true"></div>'

    return HttpResponse(html_products + html_button)
