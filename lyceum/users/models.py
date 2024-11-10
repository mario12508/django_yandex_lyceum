from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    def get_upload_path(self, filename):
        return f"uploads/{self.id}/{filename}"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )
    birthday = models.DateField(
        verbose_name="день рождения",
        null=True,
        blank=True,
    )
    image = models.ImageField(
        verbose_name="Фото профиля",
        upload_to=get_upload_path,
        null=True,
        blank=True,
    )
    coffee_count = models.PositiveIntegerField(
        default=0,
        verbose_name="количество переходов по /coffee/",
    )

    class Meta:
        verbose_name = "профиль"
        verbose_name_plural = "профили"

    def __str__(self):
        return f"{self.user.username} - Профиль"


__all__ = []
