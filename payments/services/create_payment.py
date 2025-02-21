import os
from dotenv import load_dotenv
import requests
import uuid


def create_payment(order, total_price, return_url):
    load_dotenv(override=True)

    payment_session = requests.Session()
    payment_session.auth = (os.getenv('PAYMENT_SHOP_ID'), os.getenv('PAYMENT_SECRET_KEY'))
    PAYMENT_URL = os.getenv('PAYMENT_URL')

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

    headers = {
        "Idempotence-Key": str(uuid.uuid4()),
        "Content-Type": "application/json"
    }

    payment = payment_session.post(PAYMENT_URL, headers=headers, json=payment_data, timeout=5)


    if payment.status_code == 200:
        return payment.json()
    
    return None
