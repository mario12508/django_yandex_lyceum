import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import DefaultModel


def validate_text(value):
    words = ["роскошно", "превосходно"]
    lower_values = [re.sub(r"^\W+|\W+$", "", i) for i in value.lower().split()]
    if set(lower_values) & set(words):
        return
    raise ValidationError(
        "Обязательно нужно использовать слова роскошно и превосходно",
    )


def validate_slug(value):
    # Регулярное выражение для проверки разрешенных символов
    if not re.match(r"^[a-zA-Z0-9-_]+$", value):
        raise ValidationError(
            _('Slug должен содержать только буквы, цифры, "-" и "_"'),
            code="invalid_slug",
        )


class Category(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
    )
    weight = models.PositiveIntegerField(
        default=100,
        validators=[MaxValueValidator(32767)],
    )

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")

    def __str__(self):
        return self.name


class Tag(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
    )

    class Meta:
        verbose_name = _("Тег")
        verbose_name_plural = _("Теги")

    def __str__(self):
        return self.name


class Item(DefaultModel):
    text = models.TextField(validators=[validate_text], verbose_name="Текст")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
    )
    tags = models.ManyToManyField(Tag, verbose_name="Теги")

    class Meta:
        verbose_name = _("Товар")
        verbose_name_plural = _("Товары")

    def __str__(self):
        return self.name
