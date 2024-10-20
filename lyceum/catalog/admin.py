from django.contrib import admin
from sorl.thumbnail import get_thumbnail

from catalog.models import Category, Image, Item, Tag


class ImageInline(admin.TabularInline):
    model = Item.images.through
    extra = 1
    verbose_name = "Image"
    verbose_name_plural = "Images"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (Item.name.field.name, Item.is_published.field.name)
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)
    inlines = [ImageInline]

    def thumbnail(self, obj):
        if obj.main_image:
            return f'<img src="{get_thumbnail(obj.main_image, "300x300").url}" width="30" height="30" />'
        return 'No Image'

    thumbnail.allow_tags = True
    thumbnail.short_description = 'Thumbnail'


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Image)
