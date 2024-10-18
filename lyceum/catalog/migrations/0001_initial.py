# Generated by Django 4.2.9 on 2024-10-18 12:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import catalog.validators


class Migration(migrations.Migration):

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
                        help_text="Используйте только буквы, цифры, '-', '_'. "
                        "Не должно быть пустым.",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
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
                        help_text="Используйте только буквы, цифры, '-', '_'. "
                        "Не должно быть пустым.",
                        max_length=200,
                        unique=True,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
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
                    models.TextField(
                        help_text="Обязательно нужно использовать слова "
                        "роскошно или превосходно",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "превосходно", "роскошно"
                            )
                        ],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию для этого товара.",
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
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
