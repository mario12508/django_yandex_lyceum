from django.conf import settings


alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
REQUEST_COUNTER = 0


def match(text):
    return not alphabet.isdisjoint(text.lower())


def reverse_words(text):
    words = text.split()
    reversed_words = [word[::-1] for word in words if match(word)]
    return " ".join(reversed_words)


class ReverseRussianWordsMiddleware:
    def __init__(self, get_response):
        global REQUEST_COUNTER
        self.get_response = get_response
        self.REQUEST_COUNTER = REQUEST_COUNTER

    def __call__(self, request):
        global match
        self.REQUEST_COUNTER += 1
        response = self.get_response(request)
        response_content = response.content.decode("utf-8")
        if "<body>" in response_content:
            response_content = response_content.replace("<body>", "")
            response_content = response_content.replace("</body>", "")
        if settings.ALLOW_REVERSE:
            if self.REQUEST_COUNTER % 10 == 0:
                if match(response_content):
                    response.content = (reverse_words(response_content)).encode(
                        "utf-8"
                    )

        return response
