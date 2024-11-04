from django.conf import settings
from django.db import models


class Feedback(models.Model):
    text = models.CharField(
        verbose_name="Текст сообщения",
        help_text="Максимальная длина 500 символов",
        max_length=500,
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="дата и время создания",
    )
    status = models.CharField(
        verbose_name="Статус сообщения",
        help_text="может быть трёх видов: "
        "«получено», «в обработке» и «ответ дан»",
        max_length=11,
        choices=(
            ("new", "получено"),
            ("in_progress", "в обработке"),
            ("done", "ответ дан"),
        ),
        default="new",
    )

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"

    def __str__(self):
        return f"Обратная связь {self.id}"

    def get_upload_path(self, filename):
        return f"uploads/{self.feedback.id}/{filename}"


class UserProfile(models.Model):
    author = models.OneToOneField(
        Feedback,
        on_delete=models.SET_NULL,
        verbose_name="Профиль пользователя",
        related_name="feedbacks",
        null=True,
    )
    name = models.CharField(
        verbose_name="Имя пользователя",
        help_text="Максимальная длина 100 символов",
        max_length=100,
        blank=True,
        null=True,
    )
    mail = models.EmailField(
        verbose_name="Адрес электронной почты",
        help_text="Введите корректный адрес электронной почты",
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль пользователя {self.name} ({self.mail})"


class FeedbackFile(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name="Обратная связь",
    )
    file = models.FileField(
        upload_to=Feedback.get_upload_path,
        null=True,
        blank=True,
        verbose_name="Файл обратной связи",
    )

    class Meta:
        verbose_name = "Файл обратной связи"
        verbose_name_plural = "Файлы обратных связей"

    def __str__(self):
        return f"{self.feedback}"


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Пользователь",
    )
    feedback = models.ForeignKey(
        Feedback,
        verbose_name="Обратная связь",
        on_delete=models.SET_NULL,
        null=True,
    )
    timestamp = models.TimeField(auto_now_add=True, null=True)
    status_from = models.CharField(
        choices=(
            ("new", "получено"),
            ("in_progress", "в обработке"),
            ("done", "ответ дан"),
        ),
        db_column="from",
        max_length=11,
        verbose_name="Перешел из состояния",
    )
    status_to = models.CharField(
        choices=(
            ("new", "получено"),
            ("in_progress", "в обработке"),
            ("done", "ответ дан"),
        ),
        db_column="to",
        max_length=11,
        verbose_name="Перешел в состояние",
    )

    class Meta:
        verbose_name = "журнал состояния"
        verbose_name_plural = "журнал состояний"
        ordering = ("user",)

    def __str__(self) -> str:
        return f"Текущее состояние ({self.id})"


__all__ = ["Feedback"]
