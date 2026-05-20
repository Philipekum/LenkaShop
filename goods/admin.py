from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from django.utils.html import format_html

from goods.models import (Categories, LaundryFeature, ProductImage, Products,
                          Collections, Flags, Sizes, CollectionImage)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


@admin.register(LaundryFeature)
class LaundryFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview', 'order')
    readonly_fields = ('image_preview',)

    @admin.display(description="Предпросмотр")
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />', 
                obj.image.url
            )
        return "Нет изображения"


@admin.register(Products)
class ProductsAdmin(SortableAdminBase, admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    list_display = ('name', 'category', 'price', 'discount_price', 'quantity', 'image_preview')
    list_filter = ('category', 'collections', 'flag')
    search_fields = ('name', 'description')

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'description', 'compound')
        }),
        ('Цены и количество', {
            'fields': ('price', 'discount_price', 'quantity')
        }),
        ('Связи', {
            'fields': ('flag', 'sizes', 'collections', 'laundry_features', 'similar_products')
        }),
    )

    @admin.display(description="Фото")
    def image_preview(self, obj):
        if obj and obj.pk and obj.images.exists():
            first_image = obj.images.first()
            if first_image and hasattr(first_image.image, 'url'):
                return format_html(
                    '<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 3px;" />', 
                    first_image.image.url
                )
        return "—"


class CollectionImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = CollectionImage
    extra = 1
    fields = ('image', 'image_preview', 'order')
    readonly_fields = ('image_preview',)

    @admin.display(description="Предпросмотр")
    def image_preview(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return format_html(
                '<img src="{}" style="max-height: 200px; max-width: 200px;" />', 
                obj.image.url
            )
        return "Нет изображения"


@admin.register(Collections)
class CollectionsAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [CollectionImageInline]
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Flags)
class FlagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'is_active')
