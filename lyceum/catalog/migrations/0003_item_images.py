# Generated by Django 4.2.9 on 2024-10-21 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_item_mainimage"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="images",
            field=models.ManyToManyField(
                blank=True,
                related_name="items",
                to="catalog.image",
                verbose_name="дополнительные изображения",
            ),
        ),
    ]
