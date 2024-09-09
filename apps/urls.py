from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.apartment.views import *
from apps.users.views import *
from apps.booking.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="First API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@local.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()
router.register(r'apartments', ApartmentViewSet, basename='apartments')
router.register(r'apartment-management', ApartmentManagementViewSet, basename='apartment-management')
router.register(r'users', UserViewSet, basename='users')
router.register(r'bookings', BookingViewSet)


urlpatterns = [

    # Simple JWT:
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin'),
    path('protected/', ProtectedDataView.as_view(), name='protected'),

    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('', include(router.urls)),
]
