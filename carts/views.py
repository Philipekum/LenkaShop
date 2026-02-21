from django.shortcuts import render
from django.views import View
from carts.models import Cart
from carts.mixins import CartMixin


class CartAddView(CartMixin, View):
    def post(self, request):
        product = self.get_validated_product(request)
        cart = self.get_cart_for_product(request, product)

        if cart:
            cart.quantity = min(cart.quantity + 1, 99)
            cart.save()
        else:
            Cart.objects.create(
                session_key=request.session.session_key,
                product=product, 
                quantity=1
            )

        cart_data = self.get_session_cart_data(request)
        return render(request, 'carts/htmx/cart_add.html', {
            'total_quantity': cart_data['total_quantity']
        })


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart = self.get_validated_cart(request,
                                       cart_id=request.POST.get("cart_id"))
        cart.delete()

        cart_data = self.get_session_cart_data(request)

        if cart_data['total_quantity'] == 0:
            return render(request, 'carts/htmx/cart_remove.html',
                          {'empty': True})

        return render(request, 'carts/htmx/cart_remove.html', {
            'empty': False,
            'cart_id': cart.id,
            'total_quantity': cart_data['total_quantity'],
            'total_price': cart_data['total_price']
        })


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart = self.get_validated_cart(request,
                                       cart_id=request.POST.get('cart_id'))
        action = request.POST.get('action')

        if action == 'increment':
            cart.quantity = min(cart.quantity + 1, 99)
        elif action == 'decrement' and cart.quantity > 1:
            cart.quantity -= 1

        cart.save()

        cart_data = self.get_session_cart_data(request)
        return render(request, 'carts/htmx/cart_change.html', {
            'cart': cart,
            'total_quantity': cart_data['total_quantity'],
            'total_price': cart_data['total_price'],
            'item_total_price': cart.products_price()
        })
