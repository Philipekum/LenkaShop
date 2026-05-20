from django.contrib import admin

from carts.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["product_display", "session_key", "quantity",
                    "created_timestamp",]
    list_filter = ["created_timestamp", "session_key", "product__name",]

    @admin.display(description="Товар")
    def product_display(self, obj):
        return str(obj.product.name)
