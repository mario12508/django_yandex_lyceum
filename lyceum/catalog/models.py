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
        "Обязательно нужно использовать слова роскошно или превосходно",
    )


def validate_slug(value):
    # Регулярное выражение для проверки разрешенных символов
    if not re.match(r"^[a-zA-Z0-9-_]+$", value):
        raise ValidationError(
            _('Слаг должен содержать только буквы, цифры, "-" и "_"'),
            code="invalid_slug",
        )


class Category(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text="Используйте только буквы, "
        "цифры, '-', '_'. Не должно быть пустым.",
    )
    weight = models.PositiveIntegerField(
        default=100,
        validators=[MaxValueValidator(32767)],
        verbose_name="вес",
        help_text="Значение должно быть между 1 и 32767.",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Tag(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[validate_slug],
        verbose_name="слаг",
        help_text="Используйте только буквы, "
        "цифры, '-', '_'. Не должно быть пустым.",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Item(DefaultModel):
    text = models.TextField(
        validators=[validate_text],
        verbose_name="текст",
        help_text="Обязательно нужно использовать слова "
        "роскошно или превосходно",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию для этого товара.",
    )
    tags = models.ManyToManyField(Tag, verbose_name="теги")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
