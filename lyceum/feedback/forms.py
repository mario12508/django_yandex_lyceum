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
        label = {
            Feedback.name.field.name: "Имя",
            Feedback.text.field.name: "Текст обращения",
            Feedback.mail.field.name: "Почта",
        }
        help_text = {
            Feedback.name.field.name: "Максимум 100 символов",
            Feedback.text.field.name: "Максимум 500 символов",
            Feedback.mail.field.name: "Введите корректный "
            "адрес электронной почты",
        }

    name = forms.CharField(
        label="Имя",
        widget=forms.TextInput(),
        max_length=100,
        help_text="Максимум 100 символов",
    )
    text = forms.CharField(
        label="Текст обращения",
        widget=forms.Textarea(),
        max_length=500,
        help_text="Максимум 500 символов",
    )
    mail = forms.EmailField(
        label="Почта",
        widget=forms.EmailInput(),
        max_length=150,
        help_text="Введите корректный адрес электронной почты",
    )
