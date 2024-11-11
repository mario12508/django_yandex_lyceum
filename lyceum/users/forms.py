from django import forms
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
import django.contrib.auth.models as auth_models

from users.models import Profile, User


class SignUpForm(auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(auth.forms.UserCreationForm.Meta):
        fields = [
            auth_models.User.email.field.name,
            auth_models.User.username.field.name,
            "password1",
            "password2",
        ]


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.birthday:
            self.initial["birthday"] = self.instance.birthday.strftime(
                "%Y-%m-%d",
            )

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Profile
        fields = [
            Profile.birthday.field.name,
            Profile.image.field.name,
        ]
        widgets = {
            Profile.birthday.field.name: forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
            ),
            Profile.coffee_count.field.name: forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
        }


class UserChangeForm(auth.forms.UserChangeForm):
    password = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(auth.forms.UserChangeForm.Meta):
        fields = [
            auth_models.User.first_name.field.name,
            auth_models.User.last_name.field.name,
            auth_models.User.email.field.name,
        ]
        exclude = [
            auth_models.User.password.field.name,
        ]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя или Email")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if "@" in username:
            user = User.objects.filter(email=username).first()
        else:
            user = User.objects.filter(username=username).first()

        if user and user.check_password(password):
            self.user_cache = user
        else:
            raise forms.ValidationError("Неправильные данные для входа.")

        return self.cleaned_data

    def get_user(self):
        return self.user_cache


__all__ = []
