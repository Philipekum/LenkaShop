from django.contrib import admin
from .models import InfoPage, MainPage, MainPageContentBox, MainPageTextBox

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'position')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_editable = ('position',)


class MainPageTextBoxInline(admin.TabularInline):
    model = MainPageTextBox
    extra = 1


class MainPageContentBoxInline(admin.TabularInline):
    model = MainPageContentBox
    extra = 1


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [MainPageTextBoxInline, MainPageContentBoxInline]
