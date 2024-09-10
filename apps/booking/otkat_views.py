from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как автора бронирования
        serializer.save(booking_user=self.request.user, booking_status='PENDING')

    def get_queryset(self):
        user = self.request.user
        if user.position == 'ADMIN':
            return Booking.objects.all()  # Администратор видит все бронирования
        return Booking.objects.filter(booking_user=user)  # Пользователь видит только свои бронирования

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm(self, request, pk=None):
        booking = self.get_object()

        # Проверка, является ли пользователь владельцем объекта
        if request.user == booking.booking_object.owner or request.user.is_staff:
            booking_serializer = self.get_serializer(booking)
            booking_serializer.confirm_booking()
            return Response({'status': 'Бронирование подтверждено и объект скрыт'},
                            status=status.HTTP_200_OK)

        return Response({'error': 'Вы не имеете права подтверждать это бронирование'},
                        status=status.HTTP_403_FORBIDDEN)
