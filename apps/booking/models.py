from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.apartment.models import Housing


class Booking(models.Model):
    """
    модель Booking - Бронирование объекта на выбранное время
    """
    BOOKING_STATUS = (
        ("CONFIRMED", "Confirmed"),
        ("PENDING", "Pending confirmation"),
        ("CANCELED", "Canceled"),
        ("UNCONFIRMED", "Unconfirmed")
    )
    booking_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    booking_date_from = models.DateField(_('Booking from'), null=True, blank=True)
    booking_date_to = models.DateField(_('Booking to'), null=True, blank=True)
    booking_object = models.OneToOneField(
        Housing,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_bookings',
        editable=False  # Запрещаем редактирование поля напрямую
    )
    created_at = models.DateTimeField(auto_now_add=True)
    booking_status = models.CharField(
        _('Status'),
        max_length=30,
        choices=BOOKING_STATUS,
        default='PENDING',
    )
    is_visible = models.BooleanField(default=True)  # Поле для управления видимостью объекта

    def __str__(self):
        return f'Время бронирования объекта с {self.booking_date_from} по {self.booking_date_to}'

    class Meta:
        verbose_name_plural = _('Bookings')
        verbose_name = _('Booking')

    def save(self, *args, **kwargs):
        # Устанавливаем владельца на основе объекта жилья перед сохранением
        if not self.owner_id:  # Проверяем, если поле owner еще не заполнено
            self.owner = self.booking_object.owner
        super().save(*args, **kwargs)  # Сохраняем бронирование

        # Присваиваем владельцу роль 'OWNER' в профиле пользователя
        if hasattr(self.owner, 'profile'):
            self.owner.profile.position = 'OWNER'
            self.owner.profile.save()
        else:
            # Если у пользователя нет профиля, можно создать профиль или обработать по-другому
            pass
