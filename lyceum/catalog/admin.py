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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    exclude = (Tag.normalized_name.field.name,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = (Category.normalized_name.field.name,)


class MainImageInline(admin.TabularInline):
    model = MainImage


class GalleryInline(admin.TabularInline):
    model = Gallery


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = (
        Item.name.field.name,
        Item.is_published.field.name,
        MainImage.img_tmb,
    )
    list_editable = (Item.is_published.field.name,)
    list_display_links = (Item.name.field.name,)
    filter_horizontal = (Item.tags.field.name,)
    inlines = [MainImageInline, GalleryInline]
    readonly_fields = ("created_at", "updated_at")


__all__ = ()
