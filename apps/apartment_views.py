from rest_framework import viewsets
from apps.apartment_serializers import *
from apps.apartment_models import *


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
