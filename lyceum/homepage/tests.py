from http import HTTPStatus

from django.db import connection
from django.db.models import QuerySet
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
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
        self.assertIn("items", response.context)

    def test_items_count(self):
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]

        self.assertIsInstance(items, QuerySet)
        self.assertEqual(items.count(), 3)

    def test_items_properties(self):
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]

        for item in items:
            with self.subTest(item=item):
                self.assertTrue(item.is_published)
                self.assertTrue(item.is_on_main)
                self.assertEqual(item.category, self.category)
                tags = list(item.tags.all())
                self.assertIn(self.tag, tags)

    def test_items_by_category_type(self):
        response = self.client.get(reverse("homepage:main"))
        items = response.context["items"]

        self.assertTrue(
            all(
                isinstance(item.category, catalog.models.Category)
                for item in items
            ),
        )
        self.assertTrue(
            all(isinstance(item, catalog.models.Item) for item in items),
        )

    def test_item_list_prefetch_related_tags(self):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse("homepage:main"))
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(
                "SELECT ... FROM catalog_tag ...",
                [query["sql"] for query in context.captured_queries],
                "Related tags were not prefetched as expected.",
            )

    def test_item_list_prefetch_related_categories(self):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse("homepage:main"))
            self.assertEqual(response.status_code, 200)
            self.assertNotIn(
                "SELECT ... FROM catalog_category ...",
                [query["sql"] for query in context.captured_queries],
                "Related categories were not prefetched as expected.",
            )


__all__ = ["StaticURLTests"]
