# Generated by Django 4.2.5 on 2023-10-17 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0035_rename_item_cartitem_menu_item_cartitem_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='name',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
