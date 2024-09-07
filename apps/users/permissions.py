from datetime import datetime
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import redirect


class IsOwnerOrVisibleOrAdmin(BasePermission):
    """
    Разрешает доступ:
    - К видимым объектам (is_visible=True) для всех пользователей.
    - К редактированию или удалению объектов только для владельца.
    - Полный доступ для администратора ко всем объектам.
    """

    def has_object_permission(self, request, view, obj):
        # Если пользователь администратор, то предоставить полный доступ
        if request.user.is_staff:
            return True

        # Разрешить безопасные методы (GET, HEAD или OPTIONS) всем, если объект видим
        if request.method in SAFE_METHODS:
            return obj.is_visible or obj.owner == request.user

        # Разрешить редактирование и удаление только владельцу
        return obj.owner == request.user


class IsAdminOrOwner(BasePermission):
    """
    Разрешение на изменение объекта только для администраторов или владельцев.
    """
    def has_object_permission(self, request, view, obj):
        # Все пользователи могут просматривать
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Только администратор или владелец может изменять объект
        return request.user.is_staff or obj.owner == request.user


# Разрешение на просмотр объекта только в рабочие часы
# class IsWorkHour(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         current_hour = datetime.now().hour
#         # Допустим, рабочие часы с 9 до 18
#         return 9 <= current_hour < 18


class CanGetStatisticPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('first_app.can_get_statistic')


class RedirectToLoginPermission(BasePermission):
    """
    Кастомный permission класс, перенаправляющий
    неаутентифицированных пользователей на страницу логина.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        else:
            # Перенаправление на страницу логина
            return False
