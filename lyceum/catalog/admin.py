from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from catalog.models import Category, Image, Item, Tag


class ItemAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"),
        label="Описание товара",
    )

    class Meta:
        model = Item
        fields = "__all__"


class ImageInline(admin.TabularInline):
    model = Item.images.through
    extra = 1
    verbose_name = "Дополнительное изображение"
    verbose_name_plural = "Дополнительные изображения"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = (
        Item.name.field.name,
        Item.is_published.field.name,
        Item.img_tmb,
    )
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)
    inlines = [ImageInline]


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Image)


__all__ = ["ImageInline", "ItemAdmin", "ItemAdminForm"]
