from catalog import views

from django.urls import path


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
]
