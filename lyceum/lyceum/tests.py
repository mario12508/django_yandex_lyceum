from django.test import Client, TestCase, override_settings


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
    def test_reverse_main_url(self):
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

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_reverse_main_url(self):
        client = Client()
        for i in range(9):
            response = client.get("")
            self.assertNotEqual(
                "яанвалГ",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("")
        self.assertNotIn("яанвалГ", response.content.decode())

    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_about_reverse(self):
        client = Client()
        for i in range(9):
            response = client.get("/about/")
            self.assertIn(
                "О проекте",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/about/")
        self.assertIn("О еткеорп", response.content.decode())

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_about_reverse(self):
        client = Client()
        for i in range(9):
            response = client.get("/about/")
            self.assertIn(
                "О проекте",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/about/")
        self.assertIn("О проекте", response.content.decode())

    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_catalog_reverse_first(self):
        client = Client()
        for i in range(9):
            response = client.get("/catalog/")
            self.assertIn(
                "Список элементов",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/catalog/")
        self.assertIn("косипС вотнемелэ", response.content.decode())

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_catalog_reverse_first(self):
        client = Client()
        for i in range(9):
            response = client.get("/catalog/")
            self.assertEqual(
                "Список элементов",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/catalog/")
        self.assertIn("косипС вотнемелэ", response.content.decode())

    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_catalog_reverse_second(self):
        client = Client()
        for i in range(9):
            response = client.get("/catalog/1/")
            self.assertIn(
                "Подробно элемент",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/catalog/1/")
        self.assertIn("онбордоП тнемелэ", response.content.decode())

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_catalog_reverse_second(self):
        client = Client()
        for i in range(9):
            response = client.get("/catalog/1/")
            self.assertIn(
                "Подробно элемент",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get("/catalog/1/")
        self.assertNotIn("онбордоП тнемелэ", response.content.decode())
