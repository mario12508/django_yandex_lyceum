from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def home(request):
    templates = "homepage/main.html"
    main_items = (
        Item.objects.filter(is_on_main=True, is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .only("name", "text", "category__name", "tags__name")
        .order_by("name")
    )
    context = {"main_items": main_items}
    return render(request, templates, context)


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee_view"]
