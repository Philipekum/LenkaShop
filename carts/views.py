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



# def cart_add(request):
#     product_id = request.POST.get("product_id")
#     product = Products.objects.get(id=product_id)

#     carts = Cart.objects.filter(request.session.session_key, product=product)

#     if carts.exists():
#         cart = carts.first()
        
#         if cart:
#             cart.quantity += 1
#             cart.save()
        
#         else:
#             Cart.objects.create(session_key=request.session.session_key, product=product, quantity=1)

#     user_cart = get_user_carts(request)
#     # cart_items_html = render_to_string('carts/templates/cart_modal.html', {'carts': user_cart})

def cart_change(request, product_id):
    ...


def cart_remove(request, product_id):
    ...
