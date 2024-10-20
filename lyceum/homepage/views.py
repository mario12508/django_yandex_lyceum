from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    templates = "main.html"
    context = {}
    return render(request, templates, context)


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)
