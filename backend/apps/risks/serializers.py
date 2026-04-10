from rest_framework import serializers
from .models import Risk

class RiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Risk
        fields = ['id', 'project', 'asset_id', 'name', 'description', 'probability', 'impact', 'treatment_strategy', 'owner']
        validators = []
        extra_kwargs = {
            'asset_id': {'required': False, 'allow_null': True},
            'description': {'required': False, 'allow_blank': True},
            'owner': {'required': False, 'allow_null': True},
        }

    def validate_probability(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("La probabilidad debe ser un número entre 1 y 5.")
        return value

    def validate_impact(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("El impacto debe ser un número entre 1 y 5.")
        return value

    def validate_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El nombre del riesgo no puede estar vacío.")
        return value.strip()