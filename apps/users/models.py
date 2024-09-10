from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager  # Импорт менеджера пользователей


class User(AbstractBaseUser, PermissionsMixin):
    """
    Модель класса пользователя

    Администратор - суперпользователь, имеет доступ к базе данных и всем правам
    Владелец (Owner) - арендодатель, может создавать, изменять объявления
    Юзер - арендатор, может просматривать объявления, резервировать объекты и давать отзывы и резюмировать

    Поля:
    ○ username (Строковое поле, уникальное, обязательно к заполнению)
    ○ first_name (строковое поле, обязательно к заполнению)
    ○ last_name (строковое поле, обязательно к заполнению)
    ○ email (поле email, уникальное, обязательное к заполнению)
    ○ phone (строковое поле, не обязательное)
    ○ is_staff (административное логическое поле, по умолчанию False)
    ○ is_active (логическое поле, по умолчанию True)
    ○ date_joined (Поле даты и времени, заполняется автоматически при создании)
    ○ last_login (Поле даты и времени, заполняется при входе в систему)
    ○ updated_at (Поле даты и времени, заполняется автоматически при всех обновлениях)
    ○ deleted_at (Поле даты и времени, заполняется только если поле deleted переходит в состояние True)
    ○ deleted (Логическое поле, по умолчанию - True)
    ○ position - тип пользователя
    """
    USER_CHOICE = (
        ('ADMIN', 'Admin'),
        ('OWNER', 'Owner'),
        ('USER', 'User')
    )
    username = models.CharField(
        _("username"),
        max_length=50,
        unique=True,
        error_messages={
            "unique": "A user with that username already exists.",
        }
    )
    first_name = models.CharField(
        _("first name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        _("last name"),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )
    email = models.EmailField(
        _("email address"),
        max_length=150,
        unique=True
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    position = models.CharField(
        max_length=15,
        choices=USER_CHOICE,
        default='USER'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "last_name",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.last_name} {self.first_name}"



