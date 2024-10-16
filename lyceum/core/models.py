from django.db import models


class DefaultModel(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )

    class Meta:
        abstract = True
