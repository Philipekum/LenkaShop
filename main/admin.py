from django.contrib import admin
from django.urls.resolvers import URLPattern
from .models import InfoPage

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
