from django import template
from django.http import Http404
from main.models import ContactInfo


register = template.Library()


@register.simple_tag
def get_contact_info() -> ContactInfo:
    contact = ContactInfo.objects.first()
    if not contact:
        raise Http404
    return contact
