from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models

from goods.models import Categories, LaundryFeature, Products


# admin.site.register(Categories)
# admin.site.register(Products)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(LaundryFeature)
class LaundryFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}
    }
    prepopulated_fields = {'slug': ('name',)}
