from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from apps.apartment.serializers import HousingSerializer
from apps.apartment.models import Housing
from apps.users.models import *
from apps.users.permissions import *


class ApartmentViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт, который разрешает пользователям просмотр или редактирование.
    """
    serializer_class = HousingSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrVisibleOrAdmin)

    def get_queryset(self):
        user = self.request.user

        # Если пользователь администратор, возвращаем все объекты
        if user.is_staff:
            return Housing.objects.all()

        # В противном случае возвращаем только видимые объекты или те, которые созданы текущим пользователем
        return Housing.objects.filter(is_visible=True) | Housing.objects.filter(owner=user)

    def perform_create(self, serializer):
        # Устанавливаем владельца объекта на текущего пользователя при создании
        serializer.save(owner=self.request.user)

