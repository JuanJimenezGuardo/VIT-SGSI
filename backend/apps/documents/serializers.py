from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError

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

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except DjangoValidationError as exc:
            raise DRFValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except DjangoValidationError as exc:
            raise DRFValidationError(exc.message_dict if hasattr(exc, 'message_dict') else exc.messages)
