from django.conf import settings
from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        verbose_name="Имя пользователя",
        help_text="Максимальная длина 100 символов",
        max_length=100,
        blank=True,
        null=True,
    )
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
    mail = models.EmailField(
        verbose_name="Адрес электронной почты",
        help_text="Введите корректный адрес электронной почты",
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
        return f"Обратная связь с {self.mail}"


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
