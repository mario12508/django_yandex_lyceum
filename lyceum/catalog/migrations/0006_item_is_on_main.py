# Generated by Django 4.2.9 on 2024-10-28 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_rename_mainimage_item_main_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="item",
            name="is_on_main",
            field=models.BooleanField(
                default=False,
                help_text="Определяет, отображается ли данный товар на главной странице.",
                verbose_name="Показывать на главной странице",
            ),
        ),
    ]
