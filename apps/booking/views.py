from datetime import datetime
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from apps.booking.serializers import *
from .models import *
from apps.booking.models import *
from apps.users.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..apartment.filters import HousingFilter


class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    """
     API эндпоинт, который разрешает пользователям просмотр объектов жилья и управление бронированиями.
    """
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrVisibleOrAdmin)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HousingFilter

    # Добавление документации для Swagger с указанием доступных параметров сортировки и фильтрации
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='sort_by',
                in_=openapi.IN_QUERY,
                description='Сортировка по цене или дате: price_asc, price_desc, date_asc, date_desc',
                type=openapi.TYPE_STRING,
                enum=['price_asc', 'price_desc', 'date_asc', 'date_desc']
            ),
            openapi.Parameter(
                name='price_min',
                in_=openapi.IN_QUERY,
                description='Введите минимальное значение цены',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='price_max',
                in_=openapi.IN_QUERY,
                description='Введите максимальное значение цены',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='rooms',
                in_=openapi.IN_QUERY,
                description='Введите число комнат',
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name='type',
                in_=openapi.IN_QUERY,
                description='Выберите тип объекта',
                type=openapi.TYPE_STRING,
                enum=[choice[0] for choice in Housing.TYPE_CHOICES]
            ),
            openapi.Parameter(
                name='keyword',
                in_=openapi.IN_QUERY,
                description='Введите ключевые слова для поиска',
                type=openapi.TYPE_STRING
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        # Получаем параметр сортировки из запроса, по умолчанию сортируем по id по убыванию
        sort_by = self.request.query_params.get('sort_by', '-id')

        # Получаем параметры дат из запроса
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        # Преобразуем даты из строкового формата в объекты datetime
        if date_from:
            date_from = datetime.strptime(date_from, '%Y-%m-%d')
        if date_to:
            date_to = datetime.strptime(date_to, '%Y-%m-%d')

        if user.is_staff:
            queryset = Housing.objects.all()
        else:
            # Список объектов, отфильтрованный по видимости и принадлежности
            queryset = Housing.objects.filter(
                Q(is_visible=True) |
                Q(owner=user) |
                Q(booking__booking_user=user)
            ).order_by('-id')

        # Фильтрация по дате бронирования
        if date_from and date_to:
            # Ищем объекты, у которых нет активного бронирования на указанные даты
            queryset = queryset.exclude(
                booking__booking_date_from__lte=date_to,
                booking__booking_date_to__gte=date_from,
                booking__booking_status="CONFIRMED"
            )

        # Реализация сортировки
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'date_asc':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'date_desc':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-id')  # Сортировка по id по умолчанию

        return queryset

    @swagger_auto_schema(
        method='POST',
        request_body=BookingSerializer,
        responses={
            201: BookingSerializer,
            400: 'Некорректные данные'
        },
        operation_description="Создание бронирования для объекта жилья"
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def book(self, request, pk=None):
        """
        Создание бронирования для объекта жилья
        """
        housing = self.get_object()

        # Проверка на существование активного бронирования на указанные даты
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            # Сохранение бронирования с указанием объекта жилья
            booking = serializer.save(
                booking_user=request.user,
                booking_object=housing,
                booking_status='PENDING'
            )
            return Response({
                'status': 'Бронирование создано',
                'booking': BookingSerializer(booking).data
            },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def confirm(self, request, pk=None):
        booking = self.get_object()

        if request.user == booking.booking_object.owner or request.user.is_staff:
            booking.booking_status = 'CONFIRMED'
            booking.booking_object.is_visible = False
            booking.booking_object.save()
            booking.save()
            return Response({'status': 'Бронирование подтверждено и объект скрыт'},
                            status=status.HTTP_200_OK)

        return Response({'error': 'Вы не имеете права подтверждать это бронирование'},
                        status=status.HTTP_403_FORBIDDEN)


class BookingManagementViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Устанавливаем текущего пользователя как автора бронирования
        serializer.save(booking_user=self.request.user, booking_status='PENDING')

    def get_queryset(self):
        user = self.request.user
        if user.position == 'ADMIN':
            return Booking.objects.all()  # Администратор видит все бронирования
        return Booking.objects.filter(booking_user=user)  # Пользователь видит только свои бронирования

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
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