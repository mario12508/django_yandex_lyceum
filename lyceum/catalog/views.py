from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


def item_list(request):
    templates = "catalog/item_list.html"
    items = (
        Item.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags")
        .only("name", "text", "category__name", "tags__name")
        .order_by("category__name")
    )
    context = {"items": items}
    return render(request, templates, context)


def item_detail(request, pk):
    templates = "catalog/item.html"
    item = get_object_or_404(
        Item.objects.filter(is_published=True)
        .select_related("category")
        .prefetch_related("tags", "images")
        .only("name", "text", "category__name", "tags__name", "images__image"),
        pk=pk,
    )
    context = {"pk": pk, "item": item}
    return render(request, templates, context)


def number_view(request, number):
    return HttpResponse(f"{number}")


__all__ = ["item_list", "item_detail", "number_view"]
