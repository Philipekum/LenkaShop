from django import template
from django.http import HttpRequest
from carts.models import Cart, CartQueryset


register = template.Library()


@register.simple_tag()
def user_carts(request: HttpRequest) -> CartQueryset:
    if not request.session.session_key:
        request.session.create()

    return Cart.objects.filter(
        session_key=request.session.session_key).select_related('product')
