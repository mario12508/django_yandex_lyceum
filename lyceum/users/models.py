from django.contrib.auth.models import (
    AbstractUser,
    UserManager as DjangoUserManager,
)
from django.db import models


class CustomUserManager(DjangoUserManager):
    def active(self):
        return self.filter(is_active=True).select_related("profile")

    def by_mail(self, email):
        return self.active().filter(email=email).first()


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class User(CustomUser):
    objects = CustomUserManager()

    class Meta:
        proxy = True

    def get_profile(self):
        return self.profile


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
