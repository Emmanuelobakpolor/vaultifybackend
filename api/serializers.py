from rest_framework import serializers
from .models import Admin, Service, Provider, Alert
from django.contrib.auth.hashers import make_password

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'adminName', 'adminEmail', 'adminRole', 'adminPassword']
        extra_kwargs = {
            'adminPassword': {'write_only': True},
            'id': {'read_only': True}  # Make id read_only
        }

    def create(self, validated_data):
        password = validated_data.get('adminPassword')
        if password:
            validated_data['adminPassword'] = make_password(password)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('adminPassword')
        if password:
            validated_data['adminPassword'] = make_password(password)
        return super().update(instance, validated_data)

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']
        extra_kwargs = {
            'id': {'read_only': True}  # Make id read_only
        }

class ProviderSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source='service', write_only=True
    )
    admin = serializers.PrimaryKeyRelatedField(
        queryset=Admin.objects.all(), write_only=True
    )
    admin_info = serializers.StringRelatedField(source='admin', read_only=True)

    class Meta:
        model = Provider
        fields = ['id', 'provider_name', 'email', 'phone', 'location', 'availability', 'service', 'service_id', 'admin', 'admin_info']
        extra_kwargs = {
            'id': {'read_only': True}  # Make id read_only
        }

class ServiceWithProvidersSerializer(serializers.ModelSerializer):
    providers = ProviderSerializer(many=True, read_only=True, source='provider_set')

    class Meta:
        model = Service
        fields = ['id', 'name', 'providers']
        extra_kwargs = {
            'id': {'read_only': True}  # Make id read_only
        }

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'title', 'category', 'message', 'public_date', 'estate', 'role', 'created_at']
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True}
        }
