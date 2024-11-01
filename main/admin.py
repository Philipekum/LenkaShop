from django.contrib import admin
from .models import InfoPage, MainPageContentBox, MainPageTextBox

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)


@admin.register(MainPageTextBox)
class MainPageTextBoxAdmin(admin.ModelAdmin):
    list_display = ('title',)


@admin.register(MainPageContentBox)
class MainPageContentBoxAdmin(admin.ModelAdmin):
    list_display = ('title',)
