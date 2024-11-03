from django import forms


class EchoForm(forms.Form):
    text = forms.CharField(
        label="Текст",
        widget=forms.Textarea(),
        max_length=500,
        help_text="Максимум 500 символов",
    )


__all__ = ["EchoForm"]
