from django import forms

from feedback.models import Feedback, FeedbackFile, FeedbackUserProfile


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class FeedbackUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FeedbackUserProfile
        fields = (
            FeedbackUserProfile.name.field.name,
            FeedbackUserProfile.mail.field.name,
        )
        labels = {
            FeedbackUserProfile.name.field.name: "Имя",
            FeedbackUserProfile.mail.field.name: "Почта",
        }
        help_texts = {
            FeedbackUserProfile.name.field.name: "Максимум 100 символов",
            FeedbackUserProfile.mail.field.name: "Введите корректный "
            "адрес электронной почты",
        }
        widgets = {
            FeedbackUserProfile.name.field.name: forms.TextInput(),
            FeedbackUserProfile.mail.field.name: forms.EmailInput(),
        }


class FeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Feedback
        fields = (Feedback.text.field.name,)
        labels = {
            Feedback.text.field.name: "Текст обращения",
        }
        help_texts = {
            Feedback.text.field.name: "Максимум 500 символов",
        }
        exclude = [
            Feedback.created_on.field.name,
            Feedback.status.field.name,
        ]
        widgets = {
            Feedback.text.field.name: forms.Textarea(),
        }


class FeedbackFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = FeedbackFile
        fields = (FeedbackFile.file.field.name,)
        labels = {
            FeedbackFile.file.field.name: "Загрузить файлы",
        }
        help_texts = {
            FeedbackFile.file.field.name: "Можно загрузить файлы",
        }
        widgets = {
            FeedbackFile.file.field.name: MultipleFileInput(
                attrs={
                    "multiple": True,
                },
            ),
        }


__all__ = ()
