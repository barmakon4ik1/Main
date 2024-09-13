from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from apps.users.permissions import *
from rest_framework.response import Response


class ApartmentManagementViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для добавления, редактирования и удаления объектов жилья.
    """
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def partial_update(self, request, *args, **kwargs):
    #     """
    #     Переопределение метода для обработки PATCH-запросов.
    #     """
    #     # Получаем объект, который нужно обновить
    #     instance = self.get_object()
    #
    #     # Проверяем, является ли пользователь владельцем объекта или администратором
    #     if not request.user.is_staff and request.user != instance.owner:
    #         return Response({'detail': 'У вас нет прав на изменение этого объекта.'}, status=status.HTTP_403_FORBIDDEN)
    #
    #     # Применяем изменения через сериализатор
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)