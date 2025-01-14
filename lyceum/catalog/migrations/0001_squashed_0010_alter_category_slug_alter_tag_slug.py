# Generated by Django 4.2.16 on 2024-10-31 17:55

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    replaces = [
        ("catalog", "0001_initial"),
        ("catalog", "0002_item_mainimage"),
        ("catalog", "0003_item_images"),
        ("catalog", "0004_alter_image_image_alter_item_text"),
        ("catalog", "0005_rename_mainimage_item_main_image"),
        ("catalog", "0006_item_is_on_main"),
        ("catalog", "0007_gallery_mainimage_alter_item_options_and_more"),
        ("catalog", "0008_alter_category_normalized_name_and_more"),
        ("catalog", "0009_alter_item_is_on_main"),
        ("catalog", "0010_alter_category_slug_alter_tag_slug"),
    ]

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Опубликован ли товар на сайте",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Используйте только буквы, цифры, '-', '_'. Не должно быть пустым.",
                        max_length=200,
                        null=True,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="нормализованное имя",
                    ),
                ),
                (
                    "weight",
                    models.PositiveIntegerField(
                        default=100,
                        help_text="Значение должно быть между 1 и 32767.",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(32767),
                        ],
                        verbose_name="вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Опубликован ли товар на сайте",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Используйте только буквы, цифры, '-', '_'. Не должно быть пустым.",
                        max_length=200,
                        null=True,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
                        null=True,
                        unique=True,
                        verbose_name="нормализованное имя",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название товара",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Опубликован ли товар на сайте",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "text",
                    django_ckeditor_5.fields.CKEditor5Field(
                        help_text="Обязательно нужно использовать слова роскошно или превосходно",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "превосходно", "роскошно"
                            )
                        ],
                        verbose_name="описание товара",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="catalog_items",
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        to="catalog.tag", verbose_name="теги"
                    ),
                ),
                (
                    "is_on_main",
                    models.BooleanField(
                        default=False,
                        verbose_name="Отображение на главной стнарице",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="MainImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="uploads/catalog/",
                        verbose_name="галерея",
                    ),
                ),
                (
                    "item",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="main_image",
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "главное изображение",
                "verbose_name_plural": "главное изображение",
            },
        ),
        migrations.CreateModel(
            name="Gallery",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "images",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="uploads/catalog/",
                        verbose_name="галерея",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        related_query_name="image",
                        to="catalog.item",
                    ),
                ),
            ],
            options={
                "verbose_name": "изображение в галерее",
                "verbose_name_plural": "изображения в галерее",
            },
        ),
    ]
