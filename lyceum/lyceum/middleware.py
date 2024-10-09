from django.conf import settings


alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")


def match(text):
    return not alphabet.isdisjoint(text.lower())


def reverse_words(text):
    words = text.split()
    reversed_words = [word[::-1] for word in words if match(word)]
    return " ".join(reversed_words)


class ReverseRussianWordsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global match
        settings.REQUEST_COUNTER += 1
        response = self.get_response(request)
        response_content = response.content.decode("utf-8")
        if settings.ALLOW_REVERSE:
            if (
                settings.REQUEST_COUNTER % 10 == 1
                and settings.REQUEST_COUNTER != 1
            ):
                if match(response_content):
                    if "<body>" in response_content:
                        response_content = response_content.replace(
                            "<body>", ""
                        )
                        response_content = response_content.replace(
                            "</body>", ""
                        )
                    response.content = (
                        reverse_words(response_content)
                    ).encode("utf-8")

        return response
