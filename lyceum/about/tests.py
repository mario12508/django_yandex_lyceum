from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class AboutURLTests(TestCase):
    def test_about(self):
        client = Client()
        url = reverse("about:about")
        response = client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)


__all__ = ()
