from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.apartment.views import *
from apps.users.views import *


router = DefaultRouter()
router.register(r'apartments', ApartmentViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [


    # Simple JWT:
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/', ReadOnlyOrAuthenticatedView.as_view(), name='admin'),
    path('protected/', ProtectedDataView.as_view(), name='protected'),


    path('', include(router.urls)),

]