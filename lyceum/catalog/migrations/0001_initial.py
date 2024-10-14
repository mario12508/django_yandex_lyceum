# Generated by Django 4.2.16 on 2024-10-13 15:32

from django.db import migrations, models
from django.db.models import deletion

import catalog.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CatalogCategory",
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
                    models.CharField(max_length=150, verbose_name="Название"),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Только цифры, латинские буквы, "
                        "символы '-' и '_'.",
                        max_length=200,
                        unique=True,
                        verbose_name="Слаг",
                    ),
                ),
                (
                    "weight",
                    models.PositiveSmallIntegerField(
                        default=100,
                        help_text="Значение от 1 до 32767",
                        verbose_name="Вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="CatalogTag",
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
                    models.CharField(max_length=150, verbose_name="Название"),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Только цифры, латинские буквы, "
                        "символы '-' и '_'.",
                        max_length=200,
                        unique=True,
                        verbose_name="Слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
            },
        ),
        migrations.CreateModel(
            name="CatalogItem",
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
                    models.CharField(max_length=150, verbose_name="Название"),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        validators=[catalog.models.validate_text],
                        verbose_name="Текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=deletion.CASCADE,
                        to="catalog.catalogcategory",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        to="catalog.catalogtag",
                        verbose_name="Теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
            },
        ),
    ]