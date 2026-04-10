from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'doc_type', 'status', 'version', 'created_at')
    list_filter = ('status', 'doc_type', 'project')
    search_fields = ('title', 'project__name')
