from django.db import models


class Feedback(models.Model):
    name = models.CharField(
        verbose_name="Имя пользователя",
        help_text="Максимальная длина 100 символов",
        max_length=100,
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

    class Meta:
        verbose_name = "Обратная связь"
        verbose_name_plural = "Обратные связи"

    def __str__(self):
        return f"Обратная связь с {self.mail}"


__all__ = ["Feedback"]
