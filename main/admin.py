from django.contrib import admin
from .models import *
from .forms import MainPageTextBoxForm

@admin.register(InfoPage)
class InfoPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'position')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)
    list_editable = ('position',)


class MainPageTextBoxInline(admin.TabularInline):
    model = MainPageTextBox
    form = MainPageTextBoxForm
    extra = 1


class MainPageContentBoxInline(admin.TabularInline):
    model = MainPageContentBox
    extra = 1


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage
    extra = 1
    fields = ('image',)


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CarouselImageInline]


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')  
    list_editable = ('is_active',)         
    list_filter = ('is_active',) 
    inlines = [MainPageTextBoxInline, MainPageContentBoxInline]
