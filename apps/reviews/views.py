from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewSerializer
from apps.booking.models import Booking
from ..apartment.models import Housing


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для управления отзывами и рейтингами объектов жилья
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Проверка, что пользователь может оставить отзыв только если он забронировал объект
        housing = serializer.validated_data['housing']
        user = self.request.user
        has_booking = Booking.objects.filter(
            booking_user=user,
            booking_object=housing,
            booking_status='CONFIRMED'
        ).exists()

        if not has_booking:
            return Response({'error': 'Вы можете оставить отзыв только для забронированных объектов'},
                            status=status.HTTP_403_FORBIDDEN)

        serializer.save(user=user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny])
    def housing_reviews(self, request, pk=None):
        """
        Получение всех отзывов для конкретного объекта жилья
        """
        housing = Housing.objects.get(pk=pk)
        reviews = Review.objects.filter(housing=housing)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)

