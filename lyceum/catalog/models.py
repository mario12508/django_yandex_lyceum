from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.safestring import mark_safe
from django_ckeditor_5.fields import CKEditor5Field
from sorl.thumbnail import get_thumbnail

from catalog.validators import ValidateMustContain
from core.models import CategoryAndTags, DefaultModel


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
        return self.name[:15]


class Tag(CategoryAndTags):
    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name[:15]


class ItemManager(models.Manager):
    def published(self):
        queryset = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )
        tags_prefetch = models.Prefetch(
            "tags",
            queryset=Tag.objects.filter(is_published=True).only("name"),
        )
        return (
            queryset.prefetch_related(tags_prefetch)
            .only("id", "name", "text", "category", "tags")
            .order_by("category__name", "name")
        )

    def on_main(self):
        queryset = (
            self.get_queryset()
            .select_related("category")
            .filter(
                is_published=True,
                is_on_main=True,
                category__is_published=True,
            )
        )
        tags_prefetch = models.Prefetch(
            "tags",
            queryset=Tag.objects.filter(is_published=True),
        )
        return (
            queryset.prefetch_related(tags_prefetch)
            .only("id", "name", "text", "category", "tags")
            .order_by("name")
        )


class Item(DefaultModel):
    objects = ItemManager()

    text = CKEditor5Field(
        verbose_name="описание товара",
        validators=[
            ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Обязательно нужно использовать слова роскошно "
        "или превосходно",
    )
    is_on_main = models.BooleanField(
        default=False,
        verbose_name="Отображение на главной стнарице",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="категория",
        related_name="catalog_items",
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name="теги",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    @property
    def get_img(self):
        return get_thumbnail(
            self.main_image.image,
            "300x300",
            crop="center",
            quality=51,
        )

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name[:15]


class MainImage(models.Model):
    image = models.ImageField(
        upload_to="uploads/catalog/",
        verbose_name="галерея",
        null=True,
        blank=True,
    )

    item = models.OneToOneField(
        Item,
        related_name="main_image",
        on_delete=models.CASCADE,
    )

    def img_tmb(self):
        if self.main_image:
            thumbnail_url = self.get_img.url
            return mark_safe(f"<img src='{thumbnail_url}' alt='Миниатюра'>")

        return "нет изображения"

    img_tmb.short_description = "превью"
    img_tmb.allow_tags = True

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главное изображение"


class Gallery(models.Model):
    images = models.ImageField(
        verbose_name="галерея",
        upload_to="uploads/catalog/",
        null=True,
        blank=True,
    )
    item = models.ForeignKey(
        Item,
        related_name="images",
        related_query_name="image",
        on_delete=models.CASCADE,
    )

    def get_image_nx300(self):
        return get_thumbnail(
            self.gallery.images,
            "x300",
            crop="center",
            quality=51,
        )

    def img_tmb(self):
        if self.gallery:
            return mark_safe(
                "<img src='{}' width='50' height='50'>".format(
                    self.gallery.images.url,
                ),
            )

        return "нет изображения"

    img_tmb.short_description = "превью"
    img_tmb.allow_tags = True

    class Meta:
        verbose_name = "изображение в галерее"
        verbose_name_plural = "изображения в галерее"


__all__ = ["Category", "Item", "Gallery", "Tag"]
