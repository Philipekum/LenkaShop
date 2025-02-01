import os
from yookassa import Configuration, Payment as YKPayment
from dotenv import load_dotenv


load_dotenv(override=True)

Configuration.account_id = os.getenv('PAYMENT_SHOP_ID')
Configuration.secret_key = os.getenv('PAYMENT_SECRET_KEY')


def create_yookassa_payment(order, total_price, return_url):
    payment_data = {
        "amount": {
            "value": str(total_price),
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "description": f"Оплата заказа #{order.order_id}"
    }

    payment = YKPayment.create(payment_data)
    
    return payment
