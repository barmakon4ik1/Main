from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from apps.users.permissions import *


class ApartmentManagementViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для добавления, редактирования и удаления объектов жилья.
    """
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
