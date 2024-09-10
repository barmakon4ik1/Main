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
    booking_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    booking_date_from = models.DateField(_('Booking from'), null=True, blank=True)
    booking_date_to = models.DateField(_('Booking to'), null=True, blank=True)
    booking_object = models.ForeignKey(Housing, on_delete=models.CASCADE, related_name='bookings')
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
        super().save(*args, **kwargs)  # Сначала сохраняем объект жилья
        # Присваиваем владельцу роль 'OWNER'
        if hasattr(self.owner, 'profile'):
            self.owner.profile.position = 'OWNER'
            self.owner.profile.save()
        else:
            # Если у пользователя нет профиля, создаем профиль или обрабатываем по-другому
            pass
