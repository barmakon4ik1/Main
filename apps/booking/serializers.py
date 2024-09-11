from apps.booking.models import *
from apps.apartment.models import *
from apps.users.serializers import *
from apps.apartment.serializers import *


class BookingSerializer(serializers.ModelSerializer):
    # Используем UserSerializer для отображения first_name и last_name
    booking_user = UserListSerializer()
    # # Вложенный сериализатор для объекта жилья
    booking_object = HousingSerializer()

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['booking_user', 'created_at']
        extra_kwargs = {
            'booking_status': {'default': 'PENDING'}
        }

    def validate(self, data):
        booking_object = self.initial_data.get('booking_object')

        # 'booking_object' есть в data?
        if 'booking_object' not in data:
            raise serializers.ValidationError("Объект бронирования не указан.")

        # Проверка на пересечение бронирований
        if data['booking_date_from'] > data['booking_date_to']:
            raise serializers.ValidationError("Дата начала бронирования не может быть позже даты окончания.")

        overlapping_bookings = Booking.objects.filter(
            booking_object=data['booking_object'],
            booking_status='CONFIRMED'
        ).exclude(
            booking_date_from__gt=data['booking_date_to']
        ).exclude(
            booking_date_to__lt=data['booking_date_from']
        )

        if overlapping_bookings.exists():
            raise serializers.ValidationError("Объект уже забронирован на выбранные даты.")

        return data

    def confirm_booking(self):
        booking = self.instance
        booking.booking_status = 'CONFIRMED'
        booking.save()

        # Скрываем объект ото всех, кроме владельца и пользователя, который забронировал объект
        housing = booking.booking_object
        housing.is_visible = False
        housing.save()

        return booking
