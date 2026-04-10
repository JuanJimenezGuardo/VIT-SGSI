from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'company', 'email', 'position', 'is_active', 'created_at')
    list_filter = ('is_active', 'company')
    search_fields = ('full_name', 'email', 'company__name')
