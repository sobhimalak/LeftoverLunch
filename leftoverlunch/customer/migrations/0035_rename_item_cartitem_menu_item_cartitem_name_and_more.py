# Generated by Django 4.2.5 on 2023-10-17 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0034_alter_allergie_name_alter_categorie_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='item',
            new_name='menu_item',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
