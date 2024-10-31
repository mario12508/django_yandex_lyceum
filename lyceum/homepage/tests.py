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
        cls.other_category = catalog.models.Category.objects.create(
            name="Бытовая техника",
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

    def test_home_status_code_and_context(self):
        response = self.client.get(reverse("homepage:main"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("items_by_category", response.context)

    def test_items_by_category_structure(self):
        response = self.client.get(reverse("homepage:main"))
        items_by_category = response.context["items_by_category"]

        self.assertIsInstance(items_by_category, dict)
        self.assertIn(self.category, items_by_category)
        self.assertNotIn(self.other_category, items_by_category)

    def test_items_by_category_content(self):
        response = self.client.get(reverse("homepage:main"))
        items_by_category = response.context["items_by_category"]

        items = items_by_category[self.category]
        self.assertEqual(len(items), 3)

        for item in items:
            with self.subTest(item=item):
                self.assertTrue(item.is_published)
                self.assertTrue(item.is_on_main)
                self.assertEqual(item.category, self.category)
                tags = list(item.tags.all())
                self.assertIn(self.tag, tags)

    def test_items_by_category_type(self):
        response = self.client.get(reverse("homepage:main"))
        items_by_category = response.context["items_by_category"]

        # Проверка типа категорий и товаров
        self.assertTrue(
            all(
                isinstance(category, catalog.models.Category)
                for category in items_by_category.keys()
            ),
        )
        for items in items_by_category.values():
            self.assertTrue(
                all(isinstance(item, catalog.models.Item) for item in items),
            )


__all__ = ["StaticURLTests"]
