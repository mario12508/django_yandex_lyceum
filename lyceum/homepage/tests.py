from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

import catalog.models


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


class HomepageViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = catalog.models.Category.objects.create(
            name="Электроника",
            is_published=True,
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Популярное",
            is_published=True,
        )

        for i in range(3):
            item = catalog.models.Item.objects.create(
                name=f"Товар {i + 1}",
                text="Описание товара роскошно",
                category=cls.category,
                is_published=True,
                is_on_main=True,
            )
            item.tags.set([cls.tag])

    def test_home_context(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("main_items", response.context)

        main_items = response.context["main_items"]

        self.assertEqual(len(main_items), 3)

        for item in main_items:
            self.assertTrue(item.is_published)
            self.assertTrue(item.is_on_main)
            self.assertEqual(item.category, self.category)
            self.assertIn(self.tag, item.tags.all())


__all__ = ["StaticURLTests"]
