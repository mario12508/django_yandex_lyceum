import re

from django.conf import settings


class ReverseRussianWordsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        settings.REQUEST_COUNTER += 1
        response = self.get_response(request)
        if not settings.ALLOW_REVERSE:
            return response

        if (
            settings.REQUEST_COUNTER % 10 == 1
            and settings.REQUEST_COUNTER != 1
        ):
            response_content = response.content.decode("utf-8")
            response.content = (
                self.reverse_russia_words(response_content)
            ).encode("utf-8")

        return response

    @staticmethod
    def reverse_russia_words(text):
        return re.sub(r"\\*[А-Яа-яёЁcуPHe]*", lambda x: x.group()[::-1], text)


__all__ = ["ReverseRussianWordsMiddleware"]
