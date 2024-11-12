import argparse

from django.contrib.auth.models import (
    AbstractUser,
    User as DefaultUser,
    UserManager as DjangoUserManager,
)
from django.core.exceptions import ValidationError
from django.db import models


def is_migration_command():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?")
    args, _ = parser.parse_known_args()

    return args.command in ["makemigrations", "migrate"]


if not is_migration_command():
    DefaultUser._meta.get_field("email")._unique = True


class CustomUserManager(DjangoUserManager):
    def active(self):
        return self.filter(is_active=True).select_related("profile")

    def by_mail(self, email):
        return self.active().filter(email=email).first()


class CustomUser(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")


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
