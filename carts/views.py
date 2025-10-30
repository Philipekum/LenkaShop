from django.views import View
from django.http import JsonResponse, HttpResponse
from goods.models import Products
from goods.templatetags.format_tags import format_price
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

        total_quantity = Cart.objects.filter(session_key=request.session.session_key).total_quantity()

        return HttpResponse(f"""
                                <span id="goods-in-cart-count" hx-swap-oob="true">{format_price(total_quantity)}</span>
                            """)


class CartRemoveView(CartMixin, View):
    def post(self, request):
        cart_id = request.POST.get("cart_id")

        try:
            cart = Cart.objects.get(id=cart_id, session_key=request.session.session_key)
            cart.delete()
            
            session_cart = Cart.objects.filter(session_key=request.session.session_key)  
            total_quantity: int = session_cart.total_quantity() 
            
            if total_quantity == 0:
                return HttpResponse(f"""
                    <span id="goods-in-cart-count" hx-swap-oob="true">0</span>
                    <span id="cart-total-price" hx-swap-oob="true">0</span>
                    <div id="order-cart" hx-swap-oob="true">
                        <br><div class="col-8 col-lg-10 me-2">Корзина пуста.</div>
                    </div>
                """)
            
            total_price: float = session_cart.total_price()
            return HttpResponse(f"""
                <span id="goods-in-cart-count" hx-swap-oob="true">{total_quantity}</span>
                <span id="cart-total-price" hx-swap-oob="true">{format_price(total_price)}</span>
                <div id="cart-item-{cart_id}" hx-swap-oob="true"></div>
            """)
        
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
        
        session_cart = Cart.objects.filter(session_key=request.session.session_key)
        total_quantity = session_cart.total_quantity()
        total_price = session_cart.total_price()
        item_total_price = cart.products_price()
        
        return HttpResponse(f"""
            <span id="goods-in-cart-count" hx-swap-oob="true">{total_quantity}</span>
            <span id="cart-total-price" hx-swap-oob="true">{format_price(total_price)}</span>
            <span id="cart-item-{cart.id}-price" hx-swap-oob="true">{format_price(item_total_price)}</span>
            <input id="cart-item-{cart.id}-quantity" hx-swap-oob="true" value="{cart.quantity}" readonly/>
        """)
    