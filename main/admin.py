from django.contrib import admin
from .models import *
from .forms import *

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
    form = MainPageContentBoxForm
    extra = 1


class CarouselImageInline(admin.TabularInline):
    model = CarouselImage
    extra = 1
    fields = ('image',)


class CarouselBlockInline(admin.TabularInline):
    model = CarouselBlock
    extra = 1


@admin.register(Carousel)
class CarouselAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [CarouselImageInline]


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')  
    list_editable = ('is_active',)         
    list_filter = ('is_active',) 
    inlines = [MainPageTextBoxInline, MainPageContentBoxInline, CarouselBlockInline]


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "email")

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
    