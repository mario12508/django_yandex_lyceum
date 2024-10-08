from django.test import Client, override_settings, TestCase

from . import middleware


class ReverseRussianWordsMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_on_10th_request(self):
        middleware.REQUEST_COUNTER = 0
        for i in range(9):
            response = self.client.get("/coffee/")
            self.assertNotIn(
                "кинйач",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = self.client.get("/coffee/")
        self.assertIn("кинйач", response.content.decode())

    @override_settings(ALLOW_REVERSE=False)
    def back_test_reverse_russian_words_on_10th_request(self):
        middleware.REQUEST_COUNTER = 0
        for _ in range(9):
            response = self.client.get("/coffee/")
            self.assertEqual("Я чайник", response.content.decode())
        response = self.client.get("/coffee/")
        self.assertEqual("Я чайник", response.content.decode())

    @override_settings(ALLOW_REVERSE=True)
    def test_reverse_disabled(self):
        middleware.REQUEST_COUNTER = 0
        for i in range(9):
            response = self.client.get("")
            self.assertNotIn(
                "яанвалГ",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = self.client.get("")
        self.assertIn("яанвалГ", response.content.decode())
