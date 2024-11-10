from django.contrib import auth
from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path(
        "login/",
        auth.views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth.views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    path(
        "signup/",
        views.signup_view,
        name="signup",
    ),
    path(
        "user_list/",
        views.user_list_view,
        name="user_list",
    ),
    path(
        "user_detail/<int:pk>",
        views.user_detail_view,
        name="user_detail",
    ),
    path(
        "profile/",
        views.profile_view,
        name="profile",
    ),
    path(
        "change-password/",
        auth.views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url="users:change-password-done",
        ),
        name="change-password",
    ),
    path(
        "change-password/done/",
        auth.views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="change-password-done",
    ),
    path(
        "reset-password/",
        auth.views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/subjects/password_reset_subject.txt",
            success_url="users:password-reset-done",
        ),
        name="reset-password",
    ),
    path(
        "reset-password/done/",
        auth.views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password-reset-done",
    ),
    path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth.views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url="users:password-reset-complete",
        ),
        name="password-reset-confirm",
    ),
    path(
        "reset-password/complete/",
        auth.views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password-reset-complete",
    ),
    path(
        "activate/<signed_username>/",
        views.activate_user_view,
        name="activate",
    ),
]
