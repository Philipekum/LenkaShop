from dotenv import load_dotenv
from app.settings import DEBUG
import os


load_dotenv(override=True)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_ip(ip):
    allowed = os.getenv('PAYMENT_WEBHOOK_ALLOWED_IP').split(',')

    if DEBUG:
        allowed.append(os.getenv('DEBUG_IP'))
    
    print(allowed)

    return ip in allowed
 