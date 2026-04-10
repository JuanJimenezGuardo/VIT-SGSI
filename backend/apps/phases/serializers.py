from rest_framework import serializers
from .models import Phase

class PhaseSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Phase
        fields = [
            'id', 'name', 'type', 'description', 'order',
            'planned_start_date', 'planned_end_date', 'actual_start_date', 'actual_end_date',
            'created_at', 'updated_at', 'project'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


