from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog.admin import ItemAdminForm
import catalog.models


class ItemModelTests(TestCase):
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.category = catalog.models.Category.objects.create(
            name="Категория",
            slug="категория",
        )
        cls.tag = catalog.models.Tag.objects.create(name="Тег", slug="тег")

    @classmethod
    def tearDown(cls):
        cls.category.delete()
        cls.tag.delete()

    def test_rich_text_field_widget(self):
        form = ItemAdminForm()
        self.assertIn(
            'class="django_ckeditor_5"',
            str(form["text"]),
            "CKEditor 5 is not applied.",
        )

    def test_item_creation_valid_text(self):
        item = catalog.models.Item(
            name="Превосходный товар",
            text="Этот товар просто превосходно!",
            category=self.category,
        )
        item.full_clean()
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


__all__ = ()
