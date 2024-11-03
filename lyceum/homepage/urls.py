from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.home, name="main"),
    path("echo/", views.echo, name="echo"),
    path("echo/submit/", views.echo_submit, name="echo_submit"),
    path("coffee/", views.coffee_view, name="coffee_view"),
]
