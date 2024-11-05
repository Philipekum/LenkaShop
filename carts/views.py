from django.views import View
from django.http import JsonResponse
from goods.models import Products
from .models import Cart
from .mixins import CartMixin


class CartAddView(CartMixin, View):
    def post(self, request):
        product_id = request.POST.get("product_id")
        product = Products.objects.get(id=product_id)
        cart = self.get_cart(request, product=product)

        if cart:
            cart.quantity += 1
            cart.save()
        
        else:
            Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

        response_data = {
            "message": "Товар добавлен в корзину",
            "cart_items_html": self.render_cart(request)
        }

        return JsonResponse(response_data)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        cart = self.get_cart(request, cart_id=cart_id)
        quantity = cart.quantity
        cart.delete()

        response_data = {
            "message": "Товар удален из корзины",
            "quantity_deleted": quantity,
            "cart_items_html": self.render_cart(request)
        }

        return JsonResponse(response_data)
