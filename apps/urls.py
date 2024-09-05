from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.apartment.apartment_views import *

router = DefaultRouter()
router.register(r'apartments', ApartmentViewSet)


urlpatterns = [
    path('', include(router.urls)),
]