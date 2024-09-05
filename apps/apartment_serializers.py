"""
Сериализаторы для моделей объекта и адреса
"""


from .apartment_models import *
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import re
from django.utils import timezone


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'postal_code', 'city', 'street', 'house_number']


class HousingSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Housing
        fields = '__all__'
        # read_only_fields = ['owner']  # Автоматическое добавление владельца объекта





class HousingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Housing
        fields = '__all__'

    # Добавляет текущую дату в поле created_at перед созданием объекта:
    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        return super().create(validated_data)