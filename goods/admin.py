from django.contrib import admin

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
    prepopulated_fields = {'slug': ('name',)}
