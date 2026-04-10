from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'phase', 'assigned_to', 'priority', 'status', 'planned_end_date')
    list_filter = ('status', 'priority', 'phase')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
