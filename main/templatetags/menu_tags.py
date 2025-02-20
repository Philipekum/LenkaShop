from django import template
from main.models import InfoPage, ContactInfo


register = template.Library()


@register.simple_tag
def header_links():
    return InfoPage.objects.filter(position__in=[1, 2])


@register.simple_tag
def footer_links():
    return InfoPage.objects.filter(position__in=[3, 4, 5, 6, 7, 8])


@register.simple_tag
def get_contact_info():
    return ContactInfo.objects.first()
