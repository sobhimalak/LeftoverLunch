# Generated by Django 4.2.5 on 2023-10-14 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0019_shippingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='complete',
            field=models.BooleanField(default=False),
        ),
    ]
