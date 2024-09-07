from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.apartment.serializers import HousingSerializer
from apps.apartment.models import Housing
from apps.users.models import *
from apps.users.permissions import *


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = HousingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrVisibleOrAdmin]  # Используем обновлённые разрешения

    # def get_permissions(self):
    #     """
    #     Позволяет динамически определить права доступа
    #     на основе текущего состояния пользователя.
    #     """
    #
    #     # Получаем текущего пользователя
    #     user = self.request.user
    #
    #     if user.is_authenticated:
    #         # Проверяем позицию пользователя
    #         if user.position == 'ADMIN':
    #             permission_classes = [IsAdminUser]
    #         elif user.position == 'OWNER':
    #             permission_classes = [IsOwnerOrVisibleOrAdmin]
    #         elif user.position == 'USER':
    #             permission_classes = [IsOwnerOrVisibleOrAdmin]
    #         else:
    #             permission_classes = [AllowAny]
    #     else:
    #         permission_classes = [RedirectToLoginPermission]  # Для неаутентифицированных пользователей
    #
    #         # Возвращаем соответствующий список пермишенов
    #     return [permission() for permission in permission_classes]

    # def perform_create(self, serializer):
    #     # Устанавливаем владельца объекта на текущего пользователя
    #     serializer.save(owner=self.request.user)

    # def get_queryset(self):
    #     user = self.request.user
    #     # Возвращаем только объекты с Is_visible=True
    #     return Housing.objects.filter(is_visible=True) | Housing.objects.filter(owner=user)

    def get_queryset(self):
        user = self.request.user
        # Если пользователь администратор, возвращаем все объекты
        if user.is_staff:
            return Housing.objects.all()

        # В противном случае возвращаем только видимые объекты или те, которые созданы текущим пользователем
        return Housing.objects.filter(is_visible=True) | Housing.objects.filter(owner=user)
