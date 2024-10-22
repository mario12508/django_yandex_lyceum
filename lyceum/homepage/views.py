from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone


def home(request):
    templates = "homepage/main.html"
    current_year = timezone.now().year
    context = {"current_year": current_year}
    return render(request, templates, context)


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee_view"]
