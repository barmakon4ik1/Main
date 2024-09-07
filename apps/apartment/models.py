"""
Модели для объекта недвижимости.

Включают в себя модели Address и Housing
***
Адрес состоит из полей:
country - название страны
city - населенный пункт
street - улица
house_number - номер дома (может быть с буквой и т.п. - до 6 символов)
postal_code - почтовый индекс
***
Объект недвижимости Housing имеет поля:
name - наименование объекта
description - описание объекта
price - цена аренды объекта за сутки
rooms - число комнат
type - тип объекта
address - ссылка на класс адреса объекта
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User


class Address(models.Model):
    """
    модель Address
    """
    country = models.CharField(_('Country'), max_length=100)
    city = models.CharField(_('City'), max_length=100)
    street = models.CharField(_('Street'), max_length=100)
    house_number = models.CharField(_('Haus number'), max_length=6)
    postal_code = models.CharField(_('Index'), max_length=100)

    def __str__(self):
        return f'{self.street}, {self.house_number}, {self.postal_code} {self.city}, {self.country}'

    class Meta:
        verbose_name_plural = _('Addresses')
        verbose_name = _('Address')


class Housing(models.Model):
    """
    модель Housing
    """
    TYPE_CHOICES = (
        ('APARTMENT', 'Apartment'),
        ('HOUSE', 'House'),
        ('STUDIO', 'Studio'),
        ('CASTLE', 'Castle')
        # другие типы жилья
    )
    objects_name = models.CharField(
        _('Name of object'),
        max_length=100
    )
    type = models.CharField(
        _('Type of object'),
        max_length=20,
        choices=TYPE_CHOICES,
        default='APARTMENT',
    )
    rooms = models.IntegerField(_('Number of rooms'), )
    description = models.TextField(_('Description'), )
    price = models.DecimalField(
        _('Price'),
        max_digits=10,
        decimal_places=2
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.CASCADE,
        null=True,
        related_name='housing',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='housings'
    )  # Связь с пользователем
    is_visible = models.BooleanField(default=True,)

    def __str__(self):
        return self.objects_name
