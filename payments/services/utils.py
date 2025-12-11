import ipaddress
from django.conf import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def validate_ip(ip, allowed_ips=None):
    if settings.DEBUG:
        return True 
    
    if allowed_ips is None:
        allowed_ips = settings.YOOKASSA_ALLOWED_IPS
    
    try:
        ip_obj = ipaddress.ip_address(ip)
        for allowed_ip in allowed_ips:
            if ip_obj in ipaddress.ip_network(allowed_ip):
                return True
        return False
    
    except ValueError:
        return False
