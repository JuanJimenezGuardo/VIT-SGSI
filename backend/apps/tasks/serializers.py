from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'phase', 'assigned_to', 'priority', 'status',
            'planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date',
            'work_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']