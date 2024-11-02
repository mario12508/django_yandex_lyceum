from django import forms
from django.contrib import admin
from django_ckeditor_5.widgets import CKEditor5Widget

from catalog.models import Category, Gallery, Item, MainImage, Tag


class ItemAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=CKEditor5Widget(config_name="extends"),
        label="Описание товара",
    )

    class Meta:
        model = Item
        fields = "__all__"


class ImageInline(admin.TabularInline):
    model = Gallery
    extra = 1
    verbose_name = "Дополнительное изображение"
    verbose_name_plural = "Дополнительные изображения"


class MainImageInline(admin.StackedInline):
    model = Item.main_image.related.related_model
    extra = 0
    verbose_name = "Главное изображение"
    verbose_name_plural = "Главное изображение"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = (
        Item.name.field.name,
        Item.is_published.field.name,
        MainImage.img_tmb,
        Gallery.img_tmb,
    )
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)
    inlines = [MainImageInline, ImageInline]
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Gallery)


__all__ = ["ImageInline", "ItemAdmin", "ItemAdminForm"]
