from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class CatalogTestCase(TestCase):
    def test_home_page_status_code(self):
        """Тест для проверки, что главная страница возвращает статус 200"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_addition(self):
        """Простой тест для проверки сложения"""
        self.assertEqual(1 + 1, 2)
