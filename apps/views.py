from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.apartment.models import *
from apps.booking.models import *
from rest_framework.views import APIView
from apps.apartment.serializers import *
from apps.booking.serializers import *
from django.db.models import Q
from datetime import datetime


class CombinedViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Возвращаем список объектов жилья
        queryset = Housing.objects.filter(Q(is_visible=True) | Q(owner=request.user))
        serializer = HousingSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        # Проверяем, какой тип данных пришел: объект жилья или бронирование
        if 'booking_object' in request.data:
            # Если пришли данные для бронирования
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(booking_user=request.user, booking_status='PENDING')
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Если пришли данные для создания нового объекта жилья
            serializer = HousingSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def confirm_booking(self, request, pk=None):
        try:
            booking = Booking.objects.get(pk=pk, booking_object__owner=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Бронирование не найдено или у вас нет прав на подтверждение.'},
                            status=status.HTTP_404_NOT_FOUND)

        booking.booking_status = 'CONFIRMED'
        booking.booking_object.is_visible = False  # Скрываем объект после подтверждения
        booking.booking_object.save()
        booking.save()
        return Response({'status': 'Бронирование подтверждено и объект скрыт'},
                        status=status.HTTP_200_OK)
