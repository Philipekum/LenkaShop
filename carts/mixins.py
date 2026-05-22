import logging
from typing import Union

from django.shortcuts import get_object_or_404
from django.http import Http404, HttpRequest

from carts.models import Cart
from goods.models import Products


logger = logging.getLogger("carts")


class CartMixin:
    NOT_FOUND = "Не указан товар"
    NOT_ID = "Товар не указан в запросе"

    def get_validated_product(self, request: HttpRequest) -> Products:
        product_id = request.POST.get("product_id")
        if not product_id:
            logger.warning(self.NOT_ID)
            raise Http404(self.NOT_ID)
        product = get_object_or_404(Products, id=product_id)
        return product

    def get_validated_cart(self, request: HttpRequest) -> Cart:
        if not request.session.session_key:
            request.session.create()

        cart_id = request.POST.get("cart_id")
        if not cart_id:
            raise Http404('cart_id не указан!')

        cart = get_object_or_404(
            Cart,
            id=cart_id,
            session_key=request.session.session_key
        )
        return cart

    def get_cart_for_product(self, request: HttpRequest, product: Products) -> Cart:
        if not request.session.session_key:
            request.session.create()
            
        cart = Cart.objects.filter(
            session_key=request.session.session_key,
            product=product
        ).first()

        if cart is None:
            raise Http404
        
        return cart

    def get_session_cart_data(self, request: HttpRequest) -> dict[str, Union[int, float]]:
        if not request.session.session_key:
            return {'total_quantity': 0, 'total_price': 0.0}
        
        session_cart = Cart.objects.filter(
            session_key=request.session.session_key
        )
        return {
            'total_quantity': session_cart.total_quantity(),
            'total_price': session_cart.total_price()
        }
