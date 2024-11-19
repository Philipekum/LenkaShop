from django import template

register = template.Library()

@register.filter
def format_price(value):
    try:
        value = int(value)
        print(f"ok: {value:,}".replace(",", " "))
        return f"{value:,} ₽".replace(",", " ")
    except (ValueError, TypeError):
        print(f'bruh: {value}')
        return value
