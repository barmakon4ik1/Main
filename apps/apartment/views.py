from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from apps.users.models import *
from apps.users.permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт, который разрешает пользователям просмотр или редактирование.
    """
    serializer_class = HousingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrVisibleOrAdmin)
    filter_backends = [DjangoFilterBackend]
    filterset_class = HousingFilter

    # Добавление документации по сортировке и подсказкам в полях фильтрации в Swagger:
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

        # Получаем параметры сортировки из запроса
        # По умолчанию сортировка по id desc
        sort_by = self.request.query_params.get('sort_by', '-id')

        # Если пользователь администратор, возвращаем все объекты
        if user.is_staff:
            queryset = Housing.objects.all()
        else:
            # В противном случае возвращаем только видимые объекты или те,
            # которые созданы текущим пользователем
            queryset = Housing.objects.filter(Q(is_visible=True) | Q(owner=user))

        # Добавляем сортировку
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'date_asc':
            queryset = queryset.order_by('created_at')
        elif sort_by == 'date_desc':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-id')  # По умолчанию сортировка по id

        return queryset

    def perform_create(self, serializer):
        # Устанавливаем владельца объекта на текущего пользователя при создании
        serializer.save(owner=self.request.user)



