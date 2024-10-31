from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


def item_list(request):
    items_by_category = {}

    for item in Item.objects.published():
        category = item.category
        if category not in items_by_category:
            items_by_category[category] = []
        items_by_category[category].append(item)

    context = {
        "items_by_category": items_by_category,
    }
    return render(request, "catalog/item_list.html", context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = get_object_or_404(
        Item.objects.published(),
        pk=pk,
    )
    context = {"pk": pk, "item": item}
    return render(request, template, context)


def number_view(request, number):
    return HttpResponse(f"{number}")


__all__ = ["item_list", "item_detail", "number_view"]
