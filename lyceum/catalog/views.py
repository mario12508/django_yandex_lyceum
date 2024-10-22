from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone


def item_list(request):
    templates = "catalog/item_list.html"
    current_year = timezone.now().year
    context = {"current_year": current_year}
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    current_year = timezone.now().year
    context = {"pk": pk, "current_year": current_year}
    return render(request, templates, context)


def number_view(request, number):
    return HttpResponse(f"{number}")


__all__ = ["item_list", "item_detail", "number_view"]
