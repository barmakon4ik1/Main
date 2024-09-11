from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор класса отзывов и рейтинга
    """
    user = serializers.StringRelatedField(read_only=True)  # Вывод имени пользователя
    housing = serializers.StringRelatedField(read_only=True)  # Вывод имени объекта жилья

    class Meta:
        model = Review
        fields = '__all__'
