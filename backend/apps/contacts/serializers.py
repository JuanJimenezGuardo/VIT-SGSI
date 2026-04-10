from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Contact
        fields = [
            'id', 'company', 'company_name', 'user', 'username', 'full_name', 'email',
            'phone', 'position', 'is_active', 'created_at', 'updated_at', 'work_notes'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
        validators = [
            UniqueTogetherValidator(
                queryset=Contact.objects.all(),
                fields=['company', 'email'],
                message='Ya existe un contacto con este email para la empresa.'
            )
        ]
