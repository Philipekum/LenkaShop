from django import forms
import re
from orders.models import DeliveryService


class CreateOrderForm(forms.Form):
    full_name = forms.CharField(label="ФИО", max_length=100, required=True)
    phone_number = forms.CharField(label="Телефон", required=True)
    email = forms.EmailField(label="E-mail", required=True)
    delivery_service = forms.ModelChoiceField(
        label="Служба доставки",
        queryset=DeliveryService.objects.filter(is_active=True),
        widget=forms.RadioSelect,
        empty_label=None,
        required=True
    )
    delivery_address = forms.CharField(label="Адрес доставки", required=True)

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        if not re.match(r"^\+?\d{10,15}$", phone):
            raise forms.ValidationError("Введите корректный номер телефона.")
        return phone
    