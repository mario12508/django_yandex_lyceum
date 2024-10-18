import unicodedata

from django.core.exceptions import ValidationError
from django.db import models

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


class DefaultModel(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="Название товара",
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Опубликован ли товар на сайте",
    )

    class Meta:
        abstract = True


class CategoryAndTags(DefaultModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="слаг",
        help_text="Используйте только буквы, цифры, "
        "'-', '_'. Не должно быть пустым.",
    )
    normalized_name = models.CharField(
        max_length=150,
        unique=True,
        editable=False,
        verbose_name="нормализованное имя",
    )

    class Meta:
        abstract = True

    def clean(self):
        self.normalized_name = normalize_name(self.name)
        if (
            self.__class__.objects.filter(normalized_name=self.normalized_name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                {
                    "name": f"{self._meta.verbose_name.capitalize()} с "
                    f"таким именем уже существует.",
                },
            )
