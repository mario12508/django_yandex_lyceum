from django.core.exceptions import ValidationError
from django.test import Client, TestCase

import catalog.models


class CatalogURLTests(TestCase):
    def test_catalog_list(self):
        client = Client()
        response = client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_catalog_detail(self):
        client = Client()
        response = client.get("/catalog/1/")
        self.assertEqual(response.status_code, 200)

    def test_number_view(self):
        client = Client()
        response = client.get("/catalog/re/123/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "123")

    def test_converter_number_view(self):
        client = Client()
        response = client.get("/catalog/converter/456/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "456")


class CatalogItemTests(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Категория 1",
            slug="категория-1",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Тег 1",
            slug="тег-1",
        )

    def test_item_creation_valid(self):
        item = catalog.models.Item(
            name="Товар 1",
            text="Этот товар просто превосходно!",
            category=self.category,
        )
        item.full_clean()
        item.save()

        self.assertEqual(item.name, "Товар 1")
        self.assertTrue(item.is_published)

    def test_item_creation_invalid_text(self):
        item = catalog.models.Item(
            name="Товар 2",
            text="Этот товар обычный.",
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_with_tags(self):
        item = catalog.models.Item.objects.create(
            name="Товар 3",
            text="Это действительно роскошно!",
            category=self.category,
        )
        item.tags.add(self.tag)

        self.assertIn(self.tag, item.tags.all())

    def test_item_creation_without_category(self):
        item = catalog.models.Item(
            name="Товар 4",
            text="Это превосходно!",
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_creation_with_empty_name(self):
        item = catalog.models.Item(
            name="",
            text="Это роскошно!",
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_category_name_normalization(self):
        category = catalog.models.Category(
            name="Тег",
            slug="slug",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="Teг",
            slug="slug2",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    def test_tag_name_normalization(self):
        tag = catalog.models.Tag(
            name="Москва",
            slug="moscow",
        )
        tag.full_clean()
        tag.save()

        similar_tag = catalog.models.Tag(
            name="Mocквa",
            slug="moscow2",
        )
        with self.assertRaises(ValidationError):
            similar_tag.full_clean()

    def test_case_insensitivity_in_normalization(self):
        category = catalog.models.Category(
            name="Москва",
            slug="moscow",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="москва",
            slug="moscow-lower",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    def test_punctuation_insensitivity_in_normalization(self):
        category = catalog.models.Category(
            name="Москва!",
            slug="moscow",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="Москва.",
            slug="moscow-dot",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    # New tests for spaces and punctuation
    def test_normalization_with_extra_spaces(self):
        category = catalog.models.Category(
            name="Москва",
            slug="moscow",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="  Москва  ",
            slug="moscow-spaces",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    def test_normalization_with_leading_and_trailing_spaces(self):
        category = catalog.models.Category(
            name="Москва",
            slug="moscow",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="Москва   ",
            slug="moscow-trailing-spaces",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    def test_normalization_with_spaces_between_words(self):
        category = catalog.models.Category(
            name="Москва",
            slug="moscow",
        )
        category.full_clean()
        category.save()

        similar_category = catalog.models.Category(
            name="М о с к в а",
            slug="moscow-between-spaces",
        )
        with self.assertRaises(ValidationError):
            similar_category.full_clean()

    def test_normalization_with_dashes_and_commas(self):
        tag = catalog.models.Tag(
            name="Москва",
            slug="moscow",
        )
        tag.full_clean()
        tag.save()

        similar_tag = catalog.models.Tag(
            name="Москва-,",
            slug="moscow-punctuation",
        )
        with self.assertRaises(ValidationError):
            similar_tag.full_clean()

    def test_normalization_with_special_characters(self):
        tag = catalog.models.Tag(
            name="Москва",
            slug="moscow",
        )
        tag.full_clean()
        tag.save()

        similar_tag = catalog.models.Tag(
            name="Москва!@#$%^&*",
            slug="moscow-special-chars",
        )
        with self.assertRaises(ValidationError):
            similar_tag.full_clean()
