from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import User
from apps.apartment.models import Housing


class Review(models.Model):
    """
    Модель Review для хранения отзывов и рейтингов пользователей для объектов жилья
    """
    RATING_CHOICES = [(i, str(i)) for i in range(0, 11)]  # Рейтинги от 1 до 10

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('User')
    ) # Связь с пользователем
    housing = models.ForeignKey(
        Housing,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name=_('Housing')
    ) # Связь с объектом жилья
    rating = models.IntegerField(
        _('Rating'),
        choices=RATING_CHOICES
    ) # Рейтинг
    comment = models.TextField(
        _('Comment'),
        blank=True,
        null=True
    ) # Комментарии и отзывы
    created_at = models.DateTimeField(auto_now_add=True) # Дата создания

    def __str__(self):
        return f'Отзыв от {self.user.first_name} {self.user.last_name} для {self.housing.objects_name}'

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at']  # Сортировка по дате создания
