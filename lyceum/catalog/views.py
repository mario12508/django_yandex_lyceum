import datetime

from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from catalog.models import Item


def item_list(request):
    items = Item.objects.published()

    context = {
        "items": items,
        "title": "Список товаров",
    }
    return render(request, "catalog/item_list.html", context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = get_object_or_404(
        Item.objects.published(),
        pk=pk,
    )

    context = {
        "item": item,
    }
    return render(request, template, context)


def number_view(request, number):
    return HttpResponse(f"{number}")


def new_items(request):
    template_name = "catalog/item_list.html"
    end_date = timezone.now()
    start_date = end_date - datetime.timedelta(weeks=1)

    items_queryset = Item.objects.published()
    recent_items = items_queryset.filter(
        created_at__range=[start_date, end_date],
    ).order_by("?")[:5]

    content = {
        "items": recent_items,
        "title": "Новинки",
    }
    return render(request, template_name, content)


def friday_items(request):
    template_name = "catalog/item_list.html"

    items_queryset = Item.objects.published()
    friday_items_list = items_queryset.filter(
        updated_at__week_day=5,
    ).order_by("updated_at")[:5]

    content = {
        "items": friday_items_list,
        "title": "Пятница",
    }
    return render(request, template_name, content)


def unverified_items(request):
    template_name = "catalog/item_list.html"
    items = Item.objects.published()
    items = items.filter(created_at=models.F("updated_at"))

    content = {
        "items": items,
        "title": "Непроверенное",
    }
    return render(request, template_name, content)


__all__ = ["item_list", "item_detail", "number_view"]
