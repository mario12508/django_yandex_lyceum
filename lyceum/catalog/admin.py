from django.contrib import admin

from catalog.models import CatalogCategory, CatalogItem, CatalogTag


class CatalogItemAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)


admin.site.register(CatalogItem, CatalogItemAdmin)
admin.site.register(CatalogTag)
admin.site.register(CatalogCategory)
