from django.test import Client, override_settings, TestCase


class ReverseRussianWordsMiddlewareTest(TestCase):
    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_reverse_russian_words_on_10th_request(self):
        client = Client()
        for i in range(9):
            response = client.get("/coffee/")
            self.assertNotIn(
                "кинйач",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/coffee/")
        self.assertIn("кинйач", response.content.decode())

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_reverse_russian_words_on_10th_request(self):
        client = Client()
        for _ in range(9):
            response = client.get("/coffee/")
            self.assertEqual("Я чайник", response.content.decode())
        response = client.get("/coffee/")
        self.assertEqual("Я чайник", response.content.decode())

    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_reverse_disabled(self):
        client = Client()
        for i in range(9):
            response = client.get("")
            self.assertNotIn(
                "яанвалГ",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("")
        self.assertIn("яанвалГ", response.content.decode())
