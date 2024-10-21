from django.contrib import admin

from catalog.models import Category, Item, Image, Tag


class ImageInline(admin.TabularInline):
    model = Item.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (Item.name.field.name, Item.is_published.field.name, Item.img_tmb)
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)
    inlines = [ImageInline]


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Image)


__all__ = ["ImageInline", "ItemAdmin"]
