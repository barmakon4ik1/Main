"""
Сериализаторы для моделей объекта и адреса
"""
from apps.apartment.models import *
from rest_framework import serializers
from apps.users.serializers import *


class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор адреса
    """
    class Meta:
        model = Address
        fields = '__all__'


class HousingSerializer(serializers.ModelSerializer):
    """
    Сериализатор жилых объектов
    """
    address = AddressSerializer()
    owner = UserListSerializer(read_only=True)

    class Meta:
        model = Housing
        fields = '__all__'
        read_only_fields = ['owner']  # Автоматическое добавление владельца объекта

    def update(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        return super().update(validated_data)

    def create(self, validated_data):
        # Извлекаем данные адреса из validated_data
        address_data = validated_data.pop('address')

        # Создаем объект Address
        address = Address.objects.create(**address_data)

        # Создаем объект Housing, используя созданный address
        housing = Housing.objects.create(address=address, **validated_data)

        return housing

    # Вместо вызова update() на объекте Address, мы вручную обновляем каждое поле
    # модели Address и сохраняем изменения.
    def update(self, instance, validated_data):
        # Получаем данные для обновления address
        address_data = validated_data.pop('address', None)

        # Обновляем поля Housing
        instance.objects_name = validated_data.get('objects_name', instance.objects_name)
        instance.type = validated_data.get('type', instance.type)
        instance.rooms = validated_data.get('rooms', instance.rooms)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.is_visible = validated_data.get('is_visible', instance.is_visible)
        instance.save()

        # Если есть данные для address, обновляем их вручную
        if address_data:
            address = instance.address  # Получаем связанный объект Address
            address.country = address_data.get('country', address.country)
            address.postal_code = address_data.get('postal_code', address.postal_code)
            address.city = address_data.get('city', address.city)
            address.street = address_data.get('street', address.street)
            address.house_number = address_data.get('house_number', address.house_number)
            address.save()

        return instance

