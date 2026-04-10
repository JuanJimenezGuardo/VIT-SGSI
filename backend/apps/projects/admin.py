from django.contrib import admin
from .models import Project, ProjectUser, ProjectContact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'status', 'planned_start_date', 'created_by']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'company__name']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(ProjectUser)
class ProjectUserAdmin(admin.ModelAdmin):
    list_display = ['project', 'user', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['project__name', 'user__username', 'user__email']


@admin.register(ProjectContact)
class ProjectContactAdmin(admin.ModelAdmin):
    list_display = ['project', 'contact', 'contact_role', 'is_primary', 'created_at']
    list_filter = ['contact_role', 'is_primary']
    search_fields = ['project__name', 'contact__full_name', 'contact__email']
