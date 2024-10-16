from django.db import models


class DefaultModel(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="Название товара",
        null=False,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Опубликован ли товар на сайте",
    )

    class Meta:
        abstract = True
