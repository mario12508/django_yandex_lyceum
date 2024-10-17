from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import unicodedata

from catalog.validators import ValidateMustContain
from core.models import DefaultModel


translit_dict = {
    "а": "a",
    "е": "e",
    "о": "o",
    "р": "p",
    "с": "c",
    "у": "y",
    "х": "x",
    "в": "b",
    "к": "k",
    "м": "m",
    "н": "h",
    "т": "t",
}


def normalize_name(value):
    normalized = unicodedata.normalize("NFKD", value).strip().lower()
    return "".join(
        translit_dict.get(char, char) for char in normalized if char.isalnum()
    )


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
    normalized_name = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name="нормализованное имя",
    )

    def clean(self):
        self.normalized_name = normalize_name(self.name)
        if (
            Category.objects.filter(normalized_name=self.normalized_name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"name": "Категория с таким именем уже существует."},
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
    normalized_name = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name="нормализованное имя",
    )

    def clean(self):
        self.normalized_name = normalize_name(self.name)
        if (
            Tag.objects.filter(normalized_name=self.normalized_name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {"name": "Тег с таким именем уже существует."},
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
