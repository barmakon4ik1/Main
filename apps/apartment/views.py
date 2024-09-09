from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import HousingSerializer
from .models import Housing
from apps.users.permissions import IsOwnerOrVisibleOrAdmin
from django_filters.rest_framework import DjangoFilterBackend
from .filters import HousingFilter
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт, который разрешает пользователям просмотр или редактирование объектов жилья.
    """
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

        # Начальное получение объектов
        if user.is_staff:
            # Администратор видит все объекты
            queryset = Housing.objects.all()
        else:
            # Пользователь видит только свои объекты, видимые объекты или те, которые он забронировал
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

    def perform_create(self, serializer):
        # Устанавливаем владельца объекта на текущего пользователя при создании
        serializer.save(owner=self.request.user)
