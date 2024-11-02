from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class CatalogURLTests(TestCase):
    def test_catalog_list(self):
        client = Client()
        url = reverse("catalog:item_list")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = ["CatalogURLTests"]
