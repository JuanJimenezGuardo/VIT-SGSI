from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'project', 'project_name', 'phase', 'task', 'title', 'doc_type',
            'status', 'file', 'version', 'approved_by', 'approved_at',
            'created_at', 'updated_at', 'planned_date', 'actual_date'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
