from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["product_display", "session_key", "quantity", "created_timestamp",]
    list_filter = ["created_timestamp", "session_key", "product__name",]

    def product_display(self, obj):
        return str(obj.product.name)
    
    product_display.short_description = "Товар"

