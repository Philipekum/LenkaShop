from django.db import transaction
from carts.models import Cart
from orders.models import Order, OrderItem, DeliveryService


class EmptyCartError(Exception):
    pass


def create_order_from_cart(
    session_key: str,
    full_name: str,
    phone_number: str,
    email: str,
    delivery_address: str,
    delivery_service: DeliveryService,
) -> tuple[Order, float]:

    cart_items = Cart.objects.filter(session_key=session_key)

    if not cart_items.exists():
        raise EmptyCartError

    with transaction.atomic():
        order = Order.objects.create(
            session_key=session_key,
            full_name=full_name,
            phone_number=phone_number,
            email=email,
            delivery_address=delivery_address,
            delivery_service=delivery_service,
        )

        total_price = 0

        for cart_item in cart_items:
            product = cart_item.product

            if product is None:
                cart_item.delete()
                continue

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
            )

            item_price = product.sell_price() * cart_item.quantity
            total_price += item_price

        order.save()

        cart_items.delete()

    return order, total_price
