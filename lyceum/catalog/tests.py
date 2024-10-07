from django.test import Client, TestCase


class CatalogURLTests(TestCase):
    def test_catalog_list(self):
        client = Client()
        response = client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_detail(self):
        client = Client()
        response = client.get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

    def test_number_view(self):
        client = Client()
        response = client.get("/re/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '123')

    def test_converter_number_view(self):
        client = Client()
        response = client.get("/converter/456")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), '456')
