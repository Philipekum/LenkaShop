from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem


class EmptyCartError(Exception):
    pass


def create_order_from_cart(
    session_key: str,
    first_name: str,
    last_name: str,
    phone_number: str,
    email: str,
    delivery_address: str
) -> tuple[Order, float]:
    
    cart_items = Cart.objects.filter(session_key=session_key)

    if not cart_items.exists():
        raise EmptyCartError

    with transaction.atomic():
        order = Order.objects.create(
            session_key=session_key,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            delivery_address=delivery_address,
        )

        total_price = 0

        for cart_item in cart_items:
            product = cart_item.product
            name = product.name
            price = product.sell_price()
            quantity = cart_item.quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                name=name,
                price=price,
                quantity=quantity,
            )
            product.quantity -= quantity
            product.save()
            total_price += price * quantity
        
        cart_items.delete()

    return order, total_price
