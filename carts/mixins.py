from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from carts.models import Cart
from goods.models import Products


class CartMixin:
    def get_validated_product(self, request):
        product_id = request.POST.get("product_id")
        if not product_id:
            return HttpResponseBadRequest("Не указан товар")
        return get_object_or_404(Products, id=product_id)

    def get_validated_cart(self, request, cart_id=None):
        if not request.session.session_key:
            request.session.create()

        if cart_id:
            return get_object_or_404(
                Cart, 
                id=cart_id,
                session_key=request.session.session_key
            )
        return None

    def get_cart_for_product(self, request, product):
        if not request.session.session_key:
            request.session.create()
        return Cart.objects.filter(
            session_key=request.session.session_key,
            product=product
        ).first()

    def get_session_cart_data(self, request):
        if not request.session.session_key:
            return {'total_quantity': 0, 'total_price': 0}

        session_cart = Cart.objects.filter(
            session_key=request.session.session_key
        )
        return {
            'total_quantity': session_cart.total_quantity(),
            'total_price': session_cart.total_price()
        }
