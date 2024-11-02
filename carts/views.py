from django.shortcuts import render


def cart(request):
    return render(request, 'carts/cart.html')


def cart_add(request, product_id):
    ...


def cart_change(request, product_id):
    ...


def cart_remove(request, product_id):
    ...
