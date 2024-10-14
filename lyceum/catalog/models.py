import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_text(value):
    if "превосходно" not in value.lower() and "роскошно" not in value.lower():
        raise ValidationError(
            _("Текст должен содержать слово " '"превосходно" или "роскошно".'),
        )


def validate_slug(value):
    # Регулярное выражение для проверки разрешенных символов
    if not re.match(r"^[a-zA-Z0-9-_]+$", value):
        raise ValidationError(
            _('Slug должен содержать только буквы, цифры, "-" и "_"'),
            code="invalid_slug",
        )


class CoreModel(models.Model):
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(CoreModel):
    name = models.CharField(max_length=150)
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


class Tag(CoreModel):
    name = models.CharField(max_length=150)
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


class Item(CoreModel):
    name = models.CharField(max_length=150)
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
