from django.test import Client, override_settings, TestCase
from django.urls import reverse


class ReverseRussianWordsMiddlewareTest(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_on_10th_request(self):
        client = Client()
        url = reverse("homepage:coffee_view")
        response = client.get(url)
        self.assertIn("кинйач", response.content.decode())

    @override_settings(ALLOW_REVERSE=False)
    def back_test_reverse_russian_words_on_10th_request(self):
        client = Client()
        url = reverse("homepage:coffee_view")
        for _ in range(9):
            response = client.get(url)
            self.assertEqual("Я чайник", response.content.decode())

        response = client.get(url)
        self.assertEqual("Я чайник", response.content.decode())


__all__ = ["ReverseRussianWordsMiddlewareTest"]
