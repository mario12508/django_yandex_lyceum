from datetime import timedelta
from http import HTTPStatus

from django.db import connection
from django.db.models import QuerySet
from django.test import Client, TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
from django.utils import timezone

import catalog.models


class CatalogViewsTests(TestCase):
    @classmethod
    def setUp(cls):
        cls.category = catalog.models.Category.objects.create(
            name="Электроника",
            is_published=True,
        )
        cls.tag1 = catalog.models.Tag.objects.create(
            name="Свежее",
            is_published=True,
        )

        cls.item = catalog.models.Item.objects.create(
            name="Тестовый товар",
            text="Это тестовый товар роскошно",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )
        cls.friday_item = catalog.models.Item.objects.create(
            name="Friday Item",
            category=cls.category,
            is_published=True,
            updated_at=timezone.now()
            - timedelta(
                days=timezone.now().weekday() + 2,
            ),
        )
        cls.friday_item.tags.add(cls.tag1)

        cls.new_item = catalog.models.Item.objects.create(
            name="New Item",
            category=cls.category,
            is_published=True,
            created_at=timezone.now() - timedelta(days=3),
        )
        cls.new_item.tags.add(cls.tag1)

        cls.unverified_item = catalog.models.Item.objects.create(
            name="Unverified Item",
            category=cls.category,
            is_published=True,
            created_at=timezone.now() - timedelta(days=30),
            updated_at=timezone.now() - timedelta(days=30),
        )
        cls.unverified_item.tags.add(cls.tag1)

        cls.main_image = catalog.models.MainImage.objects.create(
            image="items/gallery/Акция.png",
            item=cls.item,
        )

        cls.gallery_image = catalog.models.Gallery.objects.create(
            images="items/gallery/Дополнительно.png",
            item=cls.item,
        )

        cls.item.tags.set([cls.tag1])

    @classmethod
    def tearDown(cls):
        cls.category.delete()
        cls.tag1.delete()
        cls.item.delete()
        cls.friday_item.delete()
        cls.new_item.delete()
        cls.unverified_item.delete()
        cls.main_image.delete()
        cls.gallery_image.delete()

    def test_item_list_status_code(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_item_list_context_contains_items(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertIn("items", response.context)

    def test_item_list_items_are_published(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertTrue(item.is_published)

    def test_item_list_items_belong_to_correct_category(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertEqual(item.category, self.category)

    def test_item_list_items_have_correct_tags(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        for item in items:
            self.assertIn(self.tag1, item.tags.all())

    def test_item_list_contains_expected_item(self):
        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertIn(self.item, items)

    def test_item_list_prefetch_related_tags(self):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse("catalog:item_list"))
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertNotIn(
                "SELECT ... FROM catalog_tag ...",
                [query["sql"] for query in context.captured_queries],
                "Related tags were not prefetched as expected.",
            )

    def test_item_list_prefetch_related_categories(self):
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse("catalog:item_list"))
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertNotIn(
                "SELECT ... FROM catalog_category ...",
                [query["sql"] for query in context.captured_queries],
                "Related categories were not prefetched as expected.",
            )

    def test_prefetched_and_context(self):
        url = reverse("catalog:item_list")
        response = Client().get(url)
        self.assertIn("name", response.context["items"][0].__dict__)
        self.assertNotIn("is_on_main", response.context["items"][0].__dict__)
        self.assertIn(
            "tags",
            response.context["items"][0].__dict__["_prefetched_objects_cache"],
        )

    def test_item_list_count(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertEqual(len(response.context["items"]), 4)

    def test_item_list_context_type(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertIsInstance(response.context["items"], QuerySet)
        self.assertTrue(
            all(
                isinstance(item, catalog.models.Item)
                for item in response.context["items"]
            ),
        )

    def test_friday_endpoint_status(self):
        response = self.client.get(reverse("catalog:catalog_friday"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_friday_endpoint_context_items(self):
        response = self.client.get(reverse("catalog:catalog_friday"))
        self.assertIsInstance(response.context["items"], QuerySet)

    # Тесты для 'Новинки'
    def test_new_endpoint_status(self):
        response = self.client.get(reverse("catalog:catalog_new"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_new_endpoint_context_items(self):
        response = self.client.get(reverse("catalog:catalog_new"))
        self.assertIsInstance(response.context["items"], QuerySet)

    # Тесты для 'Непроверенное'
    def test_unverified_endpoint_status(self):
        response = self.client.get(reverse("catalog:catalog_unverified"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unverified_endpoint_context_items(self):
        response = self.client.get(reverse("catalog:catalog_unverified"))
        self.assertIsInstance(response.context["items"], QuerySet)


__all__ = ["CatalogViewsTests"]
