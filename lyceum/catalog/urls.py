from django.urls import path, re_path, register_converter

from catalog import converters, views

register_converter(converters.PositiveIntegerConverter, "posint")

app_name = "catalog"

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("converter/<posint:number>/", views.number_view, name="converter_view"),
    re_path(r"^re/(?P<number>0*[1-9]\d*)/$", views.number_view, name="number_view"),
]
