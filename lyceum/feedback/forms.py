from django import forms

from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        fields = (
            Feedback.name.field.name,
            Feedback.text.field.name,
            Feedback.mail.field.name,
        )
        labels = {
            Feedback.name.field.name: "Имя",
            Feedback.text.field.name: "Текст обращения",
            Feedback.mail.field.name: "Почта",
        }
        help_texts = {
            Feedback.name.field.name: "Максимум 100 символов",
            Feedback.text.field.name: "Максимум 500 символов",
            Feedback.mail.field.name: "Введите корректный "
            "адрес электронной почты",
        }
        exclude = [
            Feedback.name.field.name,
            Feedback.created_on.field.name,
            Feedback.status.field.name,
        ]
        widgets = {
            Feedback.name.field.name: forms.TextInput(),
            Feedback.text.field.name: forms.Textarea(),
            Feedback.mail.field.name: forms.EmailInput(),
        }


__all__ = ["FeedbackForm"]
