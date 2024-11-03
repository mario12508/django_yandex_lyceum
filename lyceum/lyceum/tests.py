from django.test import Client, override_settings, TestCase
from django.urls import reverse

from feedback.forms import FeedbackForm
from feedback.models import Feedback


class ReverseRussianWordsMiddlewareTest(TestCase):
    @override_settings(ALLOW_REVERSE=True, REQUEST_COUNTER=1)
    def test_reverse_russian_words_on_10th_request(self):
        client = Client()
        url = reverse("homepage:coffee_view")
        for i in range(9):
            response = client.get(url)
            self.assertNotIn(
                "кинйач",
                response.content.decode(),
                f"Failed on request {i + 1}",
            )
        response = client.get(url)
        self.assertIn("кинйач", response.content.decode())

    @override_settings(ALLOW_REVERSE=False, REQUEST_COUNTER=1)
    def back_test_reverse_russian_words_on_10th_request(self):
        client = Client()
        url = reverse("homepage:coffee_view")
        for _ in range(9):
            response = client.get(url)
            self.assertEqual("Я чайник", response.content.decode())
        response = client.get(url)
        self.assertEqual("Я чайник", response.content.decode())


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = FeedbackForm()

    def test_name_label(self):
        name_label = FormTests.form.fields["name"].label
        self.assertEqual(name_label, "Имя")

    def test_text_label(self):
        text_label = FormTests.form.fields["text"].label
        self.assertEqual(text_label, "Текст обращения")

    def test_mail_label(self):
        mail_label = FormTests.form.fields["mail"].label
        self.assertEqual(mail_label, "Почта")

    def test_create_task(self):
        feedbacks_count = Feedback.objects.count()
        form_data = {
            "name": "Иванов Иван Иванович",
            "text": "Пример текста",
            "mail": "ivanov@example.com",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("feedback:feedback"))
        self.assertEqual(Feedback.objects.count(), feedbacks_count + 1)
        self.assertTrue(
            Feedback.objects.filter(
                name="Иванов Иван Иванович",
                text="Пример текста",
                mail="ivanov@example.com",
            ).exists(),
        )

    def test_context_form(self):
        response = self.client.get(reverse("feedback:feedback"))
        feedback_form = response.context["feedback_form"]
        self.assertIsNotNone(feedback_form)


__all__ = ["ReverseRussianWordsMiddlewareTest"]
