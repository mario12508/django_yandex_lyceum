from django.test import Client, TestCase


class AboutURLTests(TestCase):
    def test_about(self):
        client = Client()
        response = client.get("/about/")
        self.assertEqual(response.status_code, 200)


__all__ = ["AboutURLTests"]
