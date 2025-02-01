from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in PaymentTransaction._meta.fields]


    list_display = ('order', 'payment_id', 'status', 'amount', 'created_at')
    search_fields = ('payment_id', 'order__order_id')
    list_filter = ('status',)
