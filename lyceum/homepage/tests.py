from django.test import Client, TestCase


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)

    def test_coffee_view(self):
        response = Client().get("/coffee")
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.content.decode(), "Я чайник")
