from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    def test_catalog_endpoint(self):
        url = reverse("homepage:main")
        response = Client().get(url)
        self.assertEqual(response.status_code, 200)

    def test_coffee_view(self):
        url = reverse("homepage:coffee_view")
        response = Client().get(url)
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertEqual(response.content.decode(), "Я чайник")


__all__ = ["StaticURLTests"]
