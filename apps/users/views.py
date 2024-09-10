from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import *
from .serializers import *
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _


class UserViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать и редактировать пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = (IsAdminUser,)


# Simple JWT
class LoginView(APIView):
    """
    Вход в систему
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            # return Response(set_jwt_cookies(request, user))

            # Создаем новый RefreshToken для пользователя
            refresh = RefreshToken.for_user(user)

            # Явно создаем AccessToken из RefreshToken
            access_token = AccessToken.for_user(user)

            # Преобразуем токены в строки для установки в куки
            access_token_str = str(access_token)
            refresh_token_str = str(refresh)

            # Получаем время истечения для access и refresh токенов
            access_expiry = datetime.utcfromtimestamp(access_token['exp'])
            refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])

            response = Response(status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token_str,
                httponly=True,
                secure=False,  # Используйте True для HTTPS
                samesite='Lax',
                expires=access_expiry
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token_str,
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )
            return response
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
     Выход мз системы
    """
    def post(self, request, *args, **kwargs):
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


class ProtectedDataView(APIView):
    """
    Защищенный просмотр
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome!",
                         "username": request.user.username,
                        "status": request.user.position,})


def set_jwt_cookies(response, user):
    """
    Сохранение токенов для передачи в запросы
    """
    # Создаем новый RefreshToken для пользователя
    refresh = RefreshToken.for_user(user)

    # Явно создаем AccessToken из RefreshToken
    access_token = AccessToken.for_user(user)

    # Преобразуем токены в строки для установки в куки
    access_token_str = str(access_token)
    refresh_token_str = str(refresh)

    # Получаем время истечения для access и refresh токенов
    access_expiry = datetime.utcfromtimestamp(access_token['exp'])
    refresh_expiry = datetime.utcfromtimestamp(refresh['exp'])

    response = Response(status=status.HTTP_200_OK)
    response.set_cookie(
        key='access_token',
        value=access_token_str,
        httponly=True,
        secure=False,  # Используйте True для HTTPS
        samesite='Lax',
        expires=access_expiry
    )
    response.set_cookie(
        key='refresh_token',
        value=refresh_token_str,
        httponly=True,
        secure=False,
        samesite='Lax',
        expires=refresh_expiry
    )


class RegisterView(APIView):
    """
    Регистрация пользователя
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = Response({
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
            set_jwt_cookies(response, user)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicView(APIView):
    """
    Публичный доступ любому
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"message": "Access to anyone"})


class PrivateView(APIView):
    """
    Частный доступ
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Hello" + request.user.username + "!"})


class AdminView(APIView):
    """
    Класс администратора
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"message": "Hello, Admin!"})


class ReadOnlyOrAuthenticatedView(APIView):
    """
    Редактирование данных возможно только после аутентификации
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        return Response({"message": "Only authenticated users can make changes!"})

    def post(self, request):
        return Response({"message": "Data created by an authenticated user!"})


