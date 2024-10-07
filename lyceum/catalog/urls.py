from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    path('converter/<posint:number>/', views.number_view),
    re_path(r"^re/(?P<number>[1-9]\d*)/$", views.number_view),
]
