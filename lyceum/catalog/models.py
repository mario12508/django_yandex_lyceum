# from django_cleanup import cleanup
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from sorl.thumbnail import ImageField

from catalog.validators import ValidateMustContain
from core.models import CategoryAndTags, DefaultModel


class Image(models.Model):
    image = ImageField(upload_to="items/gallery/")

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return f"Image {self.id}"


class Category(CategoryAndTags):
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


class Tag(CategoryAndTags):
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
    main_image = ImageField(
        upload_to="items/main/",
        blank=True,
        null=True,
        help_text="Основная крупная картинка товара, связь 1:1",
        verbose_name="главное изображение",
    )
    images = models.ManyToManyField(
        "Image",
        related_name="items",
        blank=True,
        verbose_name="дополнительные изображения",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name
