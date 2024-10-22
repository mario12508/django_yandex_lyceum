from django.shortcuts import render
from django.utils import timezone


def description(request):
    template = "about/about.html"
    current_year = timezone.now().year
    context = {"current_year": current_year}
    return render(request, template, context)


__all__ = ["description"]
