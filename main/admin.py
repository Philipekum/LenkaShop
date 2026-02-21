from django.contrib import admin

from main.models import ContactInfo


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("phone", "email")

    def has_add_permission(self, request):
        return not ContactInfo.objects.exists()
