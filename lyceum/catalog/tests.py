from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.urls import reverse

from catalog.admin import ItemAdminForm
import catalog.models


class CatalogURLTests(TestCase):
    def test_catalog_list(self):
        client = Client()
        url = reverse("catalog:item_list")
        response = client.get(url)
        self.assertEqual(response.status_code, 200)


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


class CatalogViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = catalog.models.Category.objects.create(
            name="Электроника",
            is_published=True,
        )
        cls.tag1 = catalog.models.Tag.objects.create(
            name="Свежее",
            is_published=True,
        )

        # Создание тестового товара
        cls.item = catalog.models.Item.objects.create(
            name="Тестовый товар",
            text="Это тестовый товар роскошно",
            category=cls.category,
            is_published=True,
            is_on_main=True,
        )

        # Создание главного изображения
        cls.main_image = catalog.models.MainImage.objects.create(
            image="items/gallery/Акция.png",
            item=cls.item,
        )

        # Создание изображения в галерее
        cls.gallery_image = catalog.models.Gallery.objects.create(
            images="items/gallery/Дополнительно.png",
            item=cls.item,
        )

        # Установка тегов для товара
        cls.item.tags.set([cls.tag1])

    def test_item_list_context(self):
        response = self.client.get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("items", response.context)

        items = response.context["items"]
        expected_items = {item.name: item for item in items}

        for item_name, item in expected_items.items():
            self.assertTrue(item.is_published)
            self.assertEqual(item.category, self.category)
            self.assertIn(self.tag1, item.tags.all())
            self.assertEqual(item_name, "Тестовый товар")

    def test_item_detail_context(self):
        response = self.client.get(
            reverse("catalog:item_detail", kwargs={"pk": self.item.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("item", response.context)

        item = response.context["item"]
        expected_data = {
            item.name: "Тестовый товар",
            item.category: self.category,
            item.tags.count(): 1,
            item.main_image.image.url: self.main_image.image.url,
            item.images.count(): 1,
        }
        self.assertEqual(len(list(item.tags.all())), 1)
        self.assertEqual(len(list(item.images.all())), 1)

        # Проверка значений
        for value, expected in expected_data.items():
            self.assertEqual(value, expected)

        self.assertEqual(
            item.images.first().images.url,
            self.gallery_image.images.url,
        )


__all__ = ["CatalogItemTests", "CatalogURLTests", "ItemModelTests"]
