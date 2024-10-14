from django.contrib import admin

from catalog.models import Category, Item, Tag


class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


admin.site.register(Item, CatalogItemAdmin)
admin.site.register(Tag)
admin.site.register(Category)
