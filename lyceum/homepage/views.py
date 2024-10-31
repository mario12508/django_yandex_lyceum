from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def home(request):
    templates = "homepage/main.html"
    items_by_category = {}

    for item in Item.objects.on_main():
        category = item.category
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    context = {
        "items_by_category": items_by_category,
    }
    return render(request, templates, context)


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee_view"]
