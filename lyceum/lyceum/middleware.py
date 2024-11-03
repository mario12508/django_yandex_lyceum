import re

from django.conf import settings


class ReverseRussianWordsMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_need_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        cls.count += 1
        if cls.count != 10:
            return False

        cls.count = 0
        return True

    def __call__(self, request):
        if not self.check_need_reverse():
            return self.get_response(request)

        response = self.get_response(request)
        content = response.content.decode("utf-8")
        reverse_content = self.reverse_russia_words(content)
        response.content = reverse_content.encode("utf-8")

        return response

    @staticmethod
    def reverse_russia_words(text):
        return re.sub(r"\b[а-яА-ЯёЁ]+\b", lambda x: x.group()[::-1], text)


__all__ = [ReverseRussianWordsMiddleware]
