from django.contrib import admin

from orders.models import Order, OrderItem, DeliveryService


class OrderItemTabulareAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "quantity"
    search_fields = (
        "product",
    )
    extra = 0



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "quantity"
    search_fields = (
        "order",
        "product",
    )


class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "status",
        "created_timestamp",
    )

    search_fields = (
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "full_name",
        'delivery_service',
        "status",
        "created_timestamp",
    )

    search_fields = (
        "order_id",
    )

    readonly_fields = ("created_timestamp",)

    list_filter = (
        "status",
        'delivery_service',
    )

    inlines = (OrderItemTabulareAdmin,)


@admin.register(DeliveryService)
class DeliveryServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'is_active')
    list_editable = ('is_active',)
