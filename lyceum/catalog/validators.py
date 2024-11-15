import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.html import strip_tags


@deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = words

    def __call__(self, value):
        clean_value = strip_tags(value)
        values = [
            re.sub(r"^\W+|\W+$", "", i) for i in clean_value.lower().split()
        ]
        if not set(self.words) & set(values):
            raise ValidationError(
                f"Обязательно нужно использовать одно из следующих слов: "
                f"{', '.join(self.words)}",
            )


__all__ = ()
