import re
from django import template


register = template.Library()


@register.filter
def format_phone(value):
    try:
        value = re.sub(r"\D", "", str(value))
        if len(value) == 11 and value.startswith("7"):
            return f"+7 ({value[1:4]}) {value[4:7]}-{value[7:9]}-{value[9:11]}"
        return value  
    
    except (ValueError, TypeError):
        return value
    