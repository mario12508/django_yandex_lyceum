from django.db import models


class DefaultModel(models.Model):
    name = models.CharField(max_length=150, unique=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True
