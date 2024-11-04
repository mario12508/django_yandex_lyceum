from django.core.files.uploadedfile import SimpleUploadedFile
import django.test
import django.urls

import feedback.forms
import feedback.models


class FeedbackFormTests(django.test.TestCase):

    def test_unable_create_feedback(self):
        item_count = feedback.models.Feedback.objects.count()
        form_data = {
            "name": "Тест",
            "text": "Тест",
            "mail": "notmail",
        }

        django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
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

        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
        )

        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
        )

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
        response = django.test.Client().post(
            django.urls.reverse("feedback:feedback"),
            data={
                **form_data,
                "file": [test_file],
            },
            follow=True,
        )

        self.assertRedirects(
            response,
            django.urls.reverse("feedback:feedback"),
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


__all__ = ["FeedbackFormTests"]
