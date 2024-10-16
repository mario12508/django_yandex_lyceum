from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from catalog.validators import ValidateMustContain
from core.models import DefaultModel


class Category(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Используйте только буквы, "
        "цифры, '-', '_'. Не должно быть пустым.",
    )
    weight = models.PositiveIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(32767)],
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
        validators=[ValidateMustContain("превосходно", "роскошно")],
        verbose_name="текст",
        help_text="Обязательно нужно использовать слова "
        "роскошно или превосходно",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        help_text="Выберите категорию для этого товара.",
        related_name="catalog_items",
    )
    tags = models.ManyToManyField(Tag, verbose_name="теги")

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
