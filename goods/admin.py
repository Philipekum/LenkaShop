from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from goods.models import Categories, LaundryFeature, ProductImage, Products, Collections, Flags


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(LaundryFeature)
class LaundryFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'layout', 'order')


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]


@admin.register(Collections)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    

@admin.register(Flags)
class FlagsAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'is_active')
