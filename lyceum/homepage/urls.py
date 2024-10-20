from django.urls import path

from homepage import views

app_name = "homepage"

urlpatterns = [
    path("", views.home, name="main"),
    path("coffee/", views.coffee_view),
]
