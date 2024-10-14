import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CoreModel(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Название"))
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Опубликовано"),
    )

    class Meta:
        abstract = True


def validate_text(value):
    if not re.search(r"\b(превосходно|роскошно)\b", value):
        raise ValidationError(
            'Текст должен содержать слова "превосходно" или "роскошно".',
        )


class CatalogCategory(CoreModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("Слаг"),
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )
    weight = models.PositiveSmallIntegerField(
        default=100,
        verbose_name=_("Вес"),
        help_text="Значение от 1 до 32767",
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name


class CatalogTag(CoreModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name=_("Слаг"),
        help_text="Только цифры, латинские буквы, символы '-' и '_'.",
    )

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")

    def __str__(self):
        return self.name


class CatalogItem(CoreModel):
    text = models.TextField(
        validators=[validate_text],
        verbose_name=_("Текст"),
    )
    category = models.ForeignKey(
        CatalogCategory,
        on_delete=models.CASCADE,
        verbose_name=_("Категория"),
    )
    tags = models.ManyToManyField(CatalogTag, verbose_name=_("Теги"))

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.name
