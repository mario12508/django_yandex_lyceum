from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def number_view(request, number):
    original_value = request.path.split("/")[-2]
    return HttpResponse(f"{original_value}")
