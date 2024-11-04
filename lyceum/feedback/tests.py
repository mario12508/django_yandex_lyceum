import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, override_settings, TestCase
from django.urls import reverse

import feedback.forms
import feedback.models


class StaticURLTests(TestCase):
    def test_form_in_feedback(self):
        url = reverse("feedback:feedback")
        response = Client().get(url)
        self.assertIn("form", response.context)

    def test_feedback_assert_redirect(self):
        url = reverse("feedback:feedback")
        form_data = {
            "name": "Масрель",
            "text": "Test text",
            "mail": "example_user@example.com",
        }
        response = Client().post(url, data=form_data, follow=True)
        self.assertRedirects(response, reverse("feedback:feedback"))

    def test_feedback_field_in_form(self):
        url = reverse("feedback:feedback")
        response = Client().get(url)
        self.assertContains(response, "helptext")
        self.assertContains(response, "label")

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "not_email",
        }

        Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count,
        )

    def test_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "123@l.com",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertFalse(response.context["form"].is_valid())
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class FeedbackFormTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form_author = feedback.forms.UserProfileForm()
        cls.form_content = feedback.forms.FeedbackForm()

    def test_feedback_show_correct_context(self):
        response = Client().get(
            reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)

    def test_text_label(self):
        name_label = FeedbackFormTests.form_content.fields["text"].label
        self.assertIsNotNone(name_label)

    def test_mail_label(self):
        mail_label = FeedbackFormTests.form_author.fields["mail"].label
        self.assertIsNotNone(mail_label)

    def test_help_text_label(self):
        text_help_text = (
            FeedbackFormTests.form_content.fields["text"].help_text,
        )
        self.assertIsNotNone(text_help_text)

    def test_help_mail_label(self):
        mail_help_text = FeedbackFormTests.form_author.fields["mail"].help_text
        self.assertIsNotNone(mail_help_text)

    def test_unable_create_feedback(self):
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "notmai",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )
        self.assertTrue(response.context["author_form"].has_error("mail"))

    def test_create_feedback_with_file_upload(self):
        feedback_count = feedback.models.Feedback.objects.count()
        file_count = feedback.models.FeedbackFile.objects.count()

        form_data = {
            "name": "Тест",
            "text": "Тестовый текст",
            "mail": "test@example.com",
        }
        test_file = SimpleUploadedFile(
            "test_file.txt",
            b"File content",
            content_type="text/plain",
        )
        response = Client().post(
            reverse("feedback:feedback"),
            data={
                **form_data,
                "file": [test_file],
            },
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse("feedback:feedback"),
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            feedback_count + 1,
        )

        self.assertEqual(
            feedback.models.FeedbackFile.objects.count(),
            file_count + 1,
        )
        uploaded_file = feedback.models.FeedbackFile.objects.last()
        self.assertEqual(
            uploaded_file.file.name,
            uploaded_file.file.name,
        )

    def test_feedback_form_labels_and_help_texts(self):
        form = feedback.forms.FeedbackForm()
        self.assertEqual(form.fields["text"].label, "Текст обращения")
        self.assertEqual(
            form.fields["text"].help_text,
            "Максимум 500 символов",
        )

    def test_user_profile_form_labels_and_help_texts(self):
        form = feedback.forms.UserProfileForm()
        self.assertEqual(form.fields["name"].label, "Имя")
        self.assertEqual(form.fields["mail"].label, "Почта")
        self.assertEqual(
            form.fields["name"].help_text,
            "Максимум 100 символов",
        )
        self.assertEqual(
            form.fields["mail"].help_text,
            "Введите корректный адрес электронной почты",
        )

    def test_feedback_file_form_multiple_upload(self):
        form = feedback.forms.FeedbackFileForm()
        self.assertTrue(
            form.fields["file"].widget.attrs.get("multiple"),
            "multiple file upload should be enabled",
        )


__all__ = ["FeedbackFormTests"]
