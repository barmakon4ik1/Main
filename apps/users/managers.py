from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользователей
    """
    def create_user(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Создание пользователя
        :param email: Е-мейл
        :param username: Псевдоним
        :param first_name: Имя
        :param last_name: Фамилия
        :param password: Пароль
        :param extra_fields: Проверка пароля
        :return: Возвращает объект пользователя
        """
        if not email:
            raise ValueError('Please enter the email address in the field')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None, **extra_fields):
        """
        Суперпользователь
        :param email: Е-мейл
        :param username: Псевдоним
        :param first_name: Имя
        :param last_name: Фамилия
        :param password: Пароль
        :param extra_fields: Проверка пароля
        :return: Возвращает объект администратора
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, first_name, last_name, password, **extra_fields)
