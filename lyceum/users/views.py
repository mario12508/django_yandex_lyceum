from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse

from users.forms import ProfileUpdateForm, SignUpForm, UserChangeForm
from users.models import Profile


def signup_view(request):
    template_name = "users/signup.html"
    form = SignUpForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        Profile.objects.create(
            user=user,
        )

        signer = signing.TimestampSigner()
        signed_username = signer.sign(user.username)
        activate_link = request.build_absolute_uri(
            reverse(
                "users:activate",
                kwargs={"signed_username": signed_username},
            ),
        )

        send_mail(
            subject="Активация профиля",
            message=render_to_string(
                "users/activation_email.txt",
                {"activate_link": activate_link},
            ),
            from_email=settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["email"]],
        )

        if settings.DEFAULT_USER_IS_ACTIVE:
            messages.success(
                request,
                "Вы зарегистрированы. Войдите с новыми данными",
            )
        else:
            messages.warning(
                request,
                "Вам необходимо активировать Ваш профиль. "
                "Проверьте указанную почту",
            )

        return redirect("users:login")

    context = {"form": form}
    return render(request, template_name, context)


def activate_user_view(request, signed_username):
    template_name = "users/activation_success.html"
    user_model = auth.get_user_model()
    signer = signing.TimestampSigner()

    try:
        username = signer.unsign(signed_username, max_age=3600 * 12)
        user = user_model.objects.get(username=username)
    except (signing.BadSignature, user_model.DoesNotExist):
        return HttpResponseNotFound(
            "Неверная или просроченная ссылка активации",
        )

    user.is_active = True
    user.save()

    return render(request, template_name)


@login_required
def user_list_view(request):
    users_list = Profile.objects.filter(
        user__is_active=True,
    )
    return render(request, "users/user_list.html", {"user_list": users_list})


def user_detail_view(request, pk):
    user = get_object_or_404(Profile, pk=pk)
    return render(request, "users/user_detail.html", {"user": user})


@login_required
def profile_view(request):
    template_name = "users/profile.html"
    user = request.user
    profile_form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=user.profile,
    )
    user_form = UserChangeForm(
        request.POST or None,
        instance=user,
    )
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    if (
        profile_form.is_valid()
        and user_form.is_valid()
        and request.method == "POST"
    ):
        profile_form.save()
        user_form.save()
        request.session.modified = True
        messages.success(
            request,
            "Настройки сохранены.",
        )
        return redirect("users:profile")

    return render(request, template_name, context)


__all__ = []