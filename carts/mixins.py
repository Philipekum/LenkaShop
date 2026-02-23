import logging

from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from carts.models import Cart
from goods.models import Products


logger = logging.getLogger("carts")


class CartMixin:
    NOT_FOUND = "Не указан товар"
    NOT_ID = "Товар не указан в запросе"

    def get_validated_product(self, request):
        product_id = request.POST.get("product_id")
        if not product_id:
            logger.warning(self.NOT_ID)
            return HttpResponseBadRequest(self.NOT_ID)
        try:
            product = get_object_or_404(Products, id=product_id)
            return product
        except Exception as e:
            logger.error(f"Ошибка при получении товара {product_id}: {e}")
            raise

    def get_validated_cart(self, request, cart_id=None):
        if not request.session.session_key:
            request.session.create()

        if cart_id:
            try:
                cart = get_object_or_404(
                    Cart,
                    id=cart_id,
                    session_key=request.session.session_key
                )
                return cart
            except Exception as e:
                logger.error(f"Ошибка при получении корзины {cart_id}: {e}")
                raise
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

        try:
            session_cart = Cart.objects.filter(
                session_key=request.session.session_key
            )
            return {
                'total_quantity': session_cart.total_quantity(),
                'total_price': session_cart.total_price()
            }
        except Exception as e:
            logger.error(f"Ошибка при подсчёте корзины: {e}", exc_info=True)
            return {'total_quantity': 0, 'total_price': 0}
