from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    templates = "item_list.html"
    context = {}
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "item.html"
    context = {"pk": pk}
    return render(request, templates, context)


def number_view(request, number):
    return HttpResponse(f"{number}")
