from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core import signing
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from users.models import User


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = User.objects.by_mail(username)
            else:
                user = User.objects.get(
                    username=username,
                )

            if user:
                if user.check_password(password):
                    if user.is_active:
                        user.attempts_count = 0
                        user.save()
                        return user

                    return None

                user.attempts_count += 1
                if user.attempts_count >= settings.MAX_AUTH_ATTEMPTS:
                    user.is_active = False
                    user.block_date = timezone.now()
                    if request:
                        signer = signing.TimestampSigner()
                        signed_username = signer.sign(user.username)
                        activate_link = request.build_absolute_uri(
                            reverse(
                                "users:unlock-account",
                                kwargs={
                                    "signed_username": signed_username,
                                },
                            ),
                        )

                        send_mail(
                            subject="Активация профиля",
                            message=render_to_string(
                                "users/activation_email.txt",
                                {"activate_link": activate_link},
                            ),
                            from_email=settings.EMAIL_HOST,
                            recipient_list=[user.email],
                        )

                user.save()

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


__all__ = []
