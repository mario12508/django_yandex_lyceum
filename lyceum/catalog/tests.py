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
