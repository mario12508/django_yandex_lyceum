from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse

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


class FeedbackFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()

    def test_feedback_show_correct_context(self):
        response = Client().get(
            reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context)

    def test_text_label(self):
        name_label = FeedbackFormTests.form.fields["text"].label
        self.assertIsNotNone(name_label)

    def test_mail_label(self):
        mail_label = FeedbackFormTests.form.fields["mail"].label
        self.assertIsNotNone(mail_label)

    def test_help_text_label(self):
        text_help_text = FeedbackFormTests.form.fields["text"].help_text
        self.assertIsNotNone(text_help_text)

    def test_help_mail_label(self):
        mail_help_text = FeedbackFormTests.form.fields["mail"].help_text
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
        self.assertTrue(response.context["form"].has_error("mail"))

    def test_feedback_sends_email(self):
        self.client.post(
            "/feedback/",
            data={
                "name": "Тест",
                "mail": "test@example.com",
                "text": "Тестовое сообщение",
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Тестовое сообщение", mail.outbox[0].body)


__all__ = ()
