# Generated by Django 4.2.5 on 2023-10-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0033_rename_category_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allergie',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='categorie',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
