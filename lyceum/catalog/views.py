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

    recent_items = Item.objects.published().filter(
        created_at__range=(start_date, end_date),
    ).only("id", "name", "category__name", "tags__name").order_by("?")[:5]

    content = {
        "items": recent_items,
        "title": "Новинки",
    }
    return render(request, template_name, content)


def friday_items(request):
    template_name = "catalog/item_list.html"

    friday_items_list = Item.objects.published().filter(
        updated_at__week_day=6,
    ).only(
        "id",
        "name",
        "updated_at",
        "category__name",
    ).order_by("updated_at")[:5]

    content = {
        "items": friday_items_list,
        "title": "Пятница",
    }
    return render(request, template_name, content)


def unverified_items(request):
    template_name = "catalog/item_list.html"

    items = Item.objects.published().filter(
        created_at=models.F("updated_at"),
    ).only("id", "name", "category__name")

    content = {
        "items": items,
        "title": "Непроверенное",
    }
    return render(request, template_name, content)



__all__ = ()
