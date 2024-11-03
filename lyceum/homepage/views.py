from http import HTTPStatus

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from catalog.models import Item
from homepage.forms import EchoForm


def home(request):
    templates = "homepage/main.html"
    items = Item.objects.on_main()

    context = {
        "items": items,
    }
    return render(request, templates, context)


def echo(request):
    template = "homepage/echo.html"
    echo_form = EchoForm(request.POST or None)
    if request.method == "POST":
        return HttpResponse(
            "Страница не найдена",
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )

    context = {"echo_form": echo_form}

    return render(request, template, context)


def echo_submit(request):
    if request.method == "POST":
        echo_text = request.POST.get("text")
        return HttpResponse(
            echo_text,
            status=HTTPStatus.OK,
        )

    return HttpResponse(
        "Необходимо отправить текст для обратного вызова",
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )


def coffee_view(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


__all__ = ["home", "coffee_view"]
