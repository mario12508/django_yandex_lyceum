from django.db.models.signals import post_save
from django.dispatch import receiver

import users.models


@receiver(post_save, sender=users.models.CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        users.models.Profile.objects.create(user=instance)


__all__ = ()
