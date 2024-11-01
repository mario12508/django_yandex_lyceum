from django.urls import path
from download import views

urlpatterns = [
    path("<path:file_path>", views.download_image, name="download_image"),
]
