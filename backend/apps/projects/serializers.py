from rest_framework import serializers
from .models import Project, ProjectUser, ProjectContact


class ProjectSerializer(serializers.ModelSerializer):
    # phases = PhaseSerializer(many=True, read_only=True)
    company_name = serializers.CharField(source='company.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'company', 'company_name', 'status',
            'planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date',
            'created_by', 'created_by_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by', 'created_by_name']


class ProjectUserSerializer(serializers.ModelSerializer):
    """
    Serializer para asignación de usuarios a proyectos.
    Incluye información detallada del usuario y proyecto.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    
    class Meta:
        model = ProjectUser
        fields = ['id', 'project', 'project_name', 'user', 'username', 'user_email', 'role', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectContactSerializer(serializers.ModelSerializer):
    contact_name = serializers.CharField(source='contact.full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectContact
        fields = [
            'id', 'project', 'project_name', 'contact', 'contact_name',
            'contact_role', 'is_primary', 'work_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

