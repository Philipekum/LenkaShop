from typing import Union
from django import template


register = template.Library()


@register.filter
def format_price(value: Union[str, int]) -> str:
    try:
        value = int(value)
        return f"{value:,} ₽".replace(",", " ")
    except (ValueError, TypeError):
        return str(value)
