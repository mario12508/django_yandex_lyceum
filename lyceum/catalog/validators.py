import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = words

    def __call__(self, value):
        values = [re.sub(r"^\W+|\W+$", "", i) for i in value.lower().split()]
        for i in values:
            for j in self.words:
                if j == i:
                    return
        raise ValidationError(
            "Обязательно нужно использовать слова " + ", ".join(self.words),
        )
