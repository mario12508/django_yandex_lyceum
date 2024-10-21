from django.http import HttpResponse
from django.shortcuts import render


def item_list(request):
    templates = "catalog/item_list.html"
    context = {}
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    context = {"pk": pk}
    return render(request, templates, context)


def number_view(request, number):
    return HttpResponse(f"{number}")


__all__ = ["item_list", "item_detail", "number_view"]
