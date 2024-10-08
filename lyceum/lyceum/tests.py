import os
from unittest.mock import patch

from django.test import Client, TestCase

from . import middleware, settings


class ReverseRussianWordsMiddlewareTest(TestCase):
    def setUp(self):
        self.client = Client()

    @patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "true"})
    def test_reverse_russian_words_on_10th_request(self):
        settings.ALLOW_REVERSE = True
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

    @patch.dict(os.environ, {"DJANGO_ALLOW_REVERSE": "false"})
    def test_reverse_disabled(self):
        settings.ALLOW_REVERSE = True
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
