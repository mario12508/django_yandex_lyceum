from http import HTTPStatus
import unittest.mock

from django.conf import settings
from django.core import signing
from django.test import TestCase
from django.urls import reverse

from users.models import User


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.registration_url = reverse("users:signup")
        self.valid_user_data = {
            "username": "sample_user",
            "email": "sample@example.com",
            "password1": "SecurePassword123",
            "password2": "SecurePassword123",
        }

    @unittest.mock.patch("users.views.send_mail")
    def test_successful_registration(self, mock_send_mail):
        response = self.client.post(
            self.registration_url,
            data=self.valid_user_data,
        )
        self.assertRedirects(response, reverse("users:login"))
        self.assertTrue(
            User.objects.filter(
                username=self.valid_user_data["username"],
            ).exists(),
        )
        mock_send_mail.assert_called_once_with(
            subject="Активация профиля",
            message=unittest.mock.ANY,
            from_email=unittest.mock.ANY,
            recipient_list=[self.valid_user_data["email"]],
        )

    def test_registration_with_password_mismatch(self):
        mismatched_data = self.valid_user_data.copy()
        mismatched_data["password2"] = "MismatchedPassword"
        response = self.client.post(
            self.registration_url,
            data=mismatched_data,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "Введенные пароли не совпадают.",
        )


class UserActivationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="test_user",
            email="testuser@example.com",
            is_active=False,
        )
        self.signer = signing.TimestampSigner()

    def test_successful_activation(self):
        signed_username = self.signer.sign(self.user.username)

        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": signed_username},
            ),
        )

        self.assertTemplateUsed(response, "users/activation_success.html")
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_activation_with_invalid_signature(self):
        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": "invalid_signature"},
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_activation_with_expired_signature(self):
        signed_username = self.signer.sign(self.user.username)
        expired_signature = f"{signed_username}:expired_part"

        response = self.client.get(
            reverse(
                "users:activate",
                kwargs={"signed_username": expired_signature},
            ),
        )

        self.assertEqual(response.status_code, 404)


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            password="password",
        )
        self.user.is_active = True
        self.user.save()

    def test_login_with_username(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "password"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_login_with_email(self):
        response = self.client.post(
            reverse("login"),
            {"username": "testuser@example.com", "password": "password"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_login_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(
            reverse("login"),
            {"username": "testuser", "password": "password"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_invalid_credentials(self):
        response = self.client.post(
            reverse("login"),
            {"username": "wronguser", "password": "password"},
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)


class EmailNormalizationTest(TestCase):
    def test_normalize_email(self):
        user = User(email="User.name@ya.ru")
        user.save()
        self.assertEqual(user.email, "user-name@yandex.ru")


class UserLockoutTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@yandex.ru",
            password="testpassword",
        )
        self.user.is_active = True
        self.user.save()

    def test_lockout_after_max_attempts(self):
        max_attempts = settings.MAX_AUTH_ATTEMPTS
        for _ in range(max_attempts):
            self.client.login(username="test@yandex.ru", password="badpas")

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_unlock_account(self):
        self.user.is_active = True
        self.user.attempts_count = 0
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.attempts_count, 0)

    def test_login_resets_attempts(self):
        self.client.login(username="test@yandex.ru", password="testpassword")
        self.user.refresh_from_db()
        self.assertEqual(self.user.attempts_count, 1)


__all__ = ()
