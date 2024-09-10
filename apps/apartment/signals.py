from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Housing


@receiver(post_save, sender=Housing)
def assign_owner_position(sender, instance, created, **kwargs):
    if created:
        user = instance.owner  # поле 'owner' связано с моделью User
        if hasattr(user, 'profile'):  # Если у пользователя есть профиль с полем position
            user.profile.position = 'OWNER'
            user.profile.save()
        else:
            # Если у пользователя нет профиля, добавьте обработку создания профиля
            pass