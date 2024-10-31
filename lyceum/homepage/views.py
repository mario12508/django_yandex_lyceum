from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item


def home(request):
    templates = "homepage/main.html"
    items = Item.objects.on_main()

    context = {
        "items": items,
    }
    return render(request, templates, context)


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee_view"]
