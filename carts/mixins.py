from django.template.loader import render_to_string
from .utils import get_user_carts
from .models import Cart


class CartMixin:
    def get_cart(self, request, product=None):
        query_kwargs = {"session_key": request.session.session_key}

        if product:
            query_kwargs["product"] = product
        
        return Cart.objects.filter(**query_kwargs).first()
    
    def render_cart(self, request):
        user_cart = get_user_carts(request)
        context = {"carts": user_cart}

        return render_to_string("carts/cart_modal.html", context, request=request)
    