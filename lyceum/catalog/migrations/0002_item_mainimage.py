# Generated by Django 4.2.9 on 2024-10-21 22:06

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="MainImage",
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                help_text="Основная крупная картинка товара, связь 1:1",
                null=True,
                upload_to="items/main/",
                verbose_name="главное изображение",
            ),
        ),
    ]