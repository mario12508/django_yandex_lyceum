from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

import catalog.models


class CatalogURLTests(TestCase):
    def test_catalog_list(self):
        client = Client()
        url = reverse("catalog:item_list")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_catalog_detail(self):
        client = Client()
        url = reverse("catalog:item_detail", args=[1])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_number_view(self):
        client = Client()
        url = reverse("catalog:number_view", args=[123])
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "123")

    def test_converter_number_view(self):
        client = Client()
        url = reverse("catalog:converter_view", args=[456])
        response = client.get(url)
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
        initial_count = catalog.models.Item.objects.count()
        item = catalog.models.Item(
            name="Товар 1",
            text="Этот товар просто превосходно!",
            category=self.category,
        )
        item.full_clean()
        item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            initial_count + 1,
        )

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


class ItemModelTests(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.category = catalog.models.Category.objects.create(
            name="Категория",
            slug="категория",
        )
        cls.tag = catalog.models.Tag.objects.create(name="Тег", slug="тег")

    def test_rich_text_field_widget(self):
        form = catalog.models.ItemAdminForm()
        self.assertIn(
            'class="django-ckeditor-widget"',
            str(form["text"]),
            "CKEditor is not applied.",
        )

    def test_item_creation_valid_text(self):
        item = catalog.models.Item(
            name="Превосходный товар",
            text="Этот товар просто превосходно!",
            category=self.category,
        )
        item.full_clean()  # Should not raise ValidationError
        item.save()

        self.assertEqual(catalog.models.Item.objects.count(), 1)

    def test_item_creation_missing_required_words(self):
        item = catalog.models.Item(
            name="Обычный товар",
            text="Этот товар обычный и не содержит нужных слов.",
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_with_tags(self):
        item = catalog.models.Item.objects.create(
            name="Роскошный товар",
            text="Это действительно роскошно!",
            category=self.category,
        )
        item.tags.add(self.tag)

        self.assertIn(self.tag, item.tags.all())

    def test_item_creation_without_category(self):
        item = catalog.models.Item(
            name="Товар без категории",
            text="Это действительно роскошно!",
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_creation_with_empty_name(self):
        item = catalog.models.Item(
            name="",
            text="Это действительно роскошно!",
            category=self.category,
        )
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_item_verbose_name(self):
        item = catalog.models.Item()
        self.assertEqual(
            item._meta.get_field("text").verbose_name,
            "описание товара",
        )

    def test_item_help_text(self):
        item = catalog.models.Item()
        self.assertEqual(
            item._meta.get_field("text").help_text,
            "Обязательно нужно использовать слова роскошно или превосходно",
        )

    def test_item_text_field_with_punctuation(self):
        item = catalog.models.Item(
            name="Товар с пунктуацией",
            text="Это действительно роскошно!",
            category=self.category,
        )
        item.full_clean()

    def test_item_text_field_with_extra_spaces(self):
        item = catalog.models.Item(
            name="Товар с пробелами",
            text="Это превосходно   !",
            category=self.category,
        )
        item.full_clean()

    def test_item_text_field_with_leading_trailing_spaces(self):
        item = catalog.models.Item(
            name="Товар с пробелами",
            text="   Это роскошно   ",
            category=self.category,
        )
        item.full_clean()

    def test_item_text_field_with_html_tags(self):
        item = catalog.models.Item(
            name="Товар с HTML",
            text="<b>Это роскошно!</b>",
            category=self.category,
        )
        item.full_clean()


__all__ = ["CatalogItemTests", "CatalogURLTests"]
