from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.shortcuts import redirect
from django.urls import reverse


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Автоматическое использование токенов из куки при запросах
    """
    def process_request(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                token = AccessToken(access_token)
                if datetime.utcfromtimestamp(token['exp']) < datetime.utcnow():
                    raise TokenError('Token expired')
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except TokenError:
                # Попробовать обновить access токен, если refresh токен не истек
                new_access_token = self.refresh_access_token(refresh_token)
                if new_access_token:
                    request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                    request._new_access_token = new_access_token
                else:
                    # Удалить токены из куки, если обновление не удалось
                    self.clear_cookies(request)
        elif refresh_token:
            new_access_token = self.refresh_access_token(refresh_token)
            if new_access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                request._new_access_token = new_access_token
            else:
                self.clear_cookies(request)

    def refresh_access_token(self, refresh_token):
        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            return new_access_token
        except TokenError:
            return None

    def process_response(self, request, response):
        # для обновления access-токена:
        new_access_token = getattr(request, '_new_access_token', None)
        if new_access_token:
            access_expiry = AccessToken(new_access_token)['exp']
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                secure=False, # Используйте True для HTTPS
                samesite='Lax',
                expires=datetime.utcfromtimestamp(access_expiry)
                )
        return response

    def clear_cookies(self, request):
        # Метод для удаления истекших куки
        request.COOKIES.pop('access_token', None)
        request.COOKIES.pop('refresh_token', None)


class RedirectUnauthenticatedMiddleware:
    """
    Middleware для перенаправления неаутентифицированных
    пользователей на страницу логина.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Если пользователь неаутентифицирован и запрашивает защищенный API
        if response.status_code == 403 and not request.user.is_authenticated:
            return redirect(reverse('login'))  # 'login' должно соответствовать имени URL вашей страницы логина
        return response
