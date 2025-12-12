from django.shortcuts import render
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
            Cart.objects.create(session_key=request.session.session_key, 
                              product=product, quantity=1)

        total_quantity = Cart.objects.filter(
            session_key=request.session.session_key
        ).total_quantity()

        return render(request, 'carts/htmx/cart_add.html', {
            'total_quantity': total_quantity
        })


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        try:
            cart = Cart.objects.get(id=cart_id, 
                                  session_key=request.session.session_key)
            cart.delete()
            
            session_cart = Cart.objects.filter(
                session_key=request.session.session_key
            )  
            total_quantity = session_cart.total_quantity() 
            
            if total_quantity == 0:
                return render(request, 'carts/htmx/cart_remove.html', {
                    'empty': True
                })
            
            total_price = session_cart.total_price()
            return render(request, 'carts/htmx/cart_remove.html', {
                'empty': False,
                'cart_id': cart_id,
                'total_quantity': total_quantity,
                'total_price': total_price
            })
        
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Корзина не найдена."}, status=404)


class CartChangeView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get('cart_id')
        action = request.POST.get('action') 
        
        cart = self.get_cart(request, cart_id=cart_id)
        
        if action == 'increment':
            cart.quantity += 1
        elif action == 'decrement' and cart.quantity > 1:
            cart.quantity -= 1
        
        cart.save()
        
        session_cart = Cart.objects.filter(
            session_key=request.session.session_key
        )
        total_quantity = session_cart.total_quantity()
        total_price = session_cart.total_price()
        item_total_price = cart.products_price()
        
        return render(request, 'carts/htmx/cart_change.html', {
            'cart': cart,
            'total_quantity': total_quantity,
            'total_price': total_price,
            'item_total_price': item_total_price
        })
