# Generated by Django 4.2.16 on 2024-11-04 21:08

from django.db import migrations, models
import django.db.models.deletion
import feedback.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "feedback",
            "0004_alter_feedback_name_alter_statuslog_feedback_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feedback",
            name="mail",
        ),
        migrations.RemoveField(
            model_name="feedback",
            name="name",
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        help_text="Максимальная длина 100 символов",
                        max_length=100,
                        null=True,
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "mail",
                    models.EmailField(
                        help_text="Введите корректный адрес электронной почты",
                        max_length=254,
                        verbose_name="Адрес электронной почты",
                    ),
                ),
                (
                    "author",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="feedbacks",
                        to="feedback.feedback",
                        verbose_name="Профиль пользователя",
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль пользователя",
                "verbose_name_plural": "Профили пользователей",
            },
        ),
        migrations.CreateModel(
            name="FeedbackFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=feedback.models.Feedback.get_upload_path,
                        verbose_name="Файл обратной связи",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to="feedback.feedback",
                        verbose_name="Обратная связь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Файл обратной связи",
                "verbose_name_plural": "Файлы обратных связей",
            },
        ),
    ]
