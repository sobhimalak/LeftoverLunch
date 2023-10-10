# Generated by Django 4.2.5 on 2023-10-06 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0014_menuitem_amount_left'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='collect_time_end',
            field=models.CharField(choices=[('11:00', '11:00 AM'), ('11:15', '11:15 AM'), ('11:30', '11:30 AM'), ('11:45', '11:45 AM'), ('12:00', '12:00 PM'), ('12:15', '12:15 PM'), ('12:30', '12:30 PM'), ('12:45', '12:45 PM'), ('13:00', '1:00 PM'), ('13:15', '1:15 PM'), ('13:30', '1:30 PM'), ('13:45', '1:45 PM'), ('14:00', '2:00 PM'), ('14:15', '2:15 PM'), ('14:30', '2:30 PM'), ('14:45', '2:45 PM'), ('15:00', '3:00 PM'), ('15:15', '3:15 PM'), ('15:30', '3:30 PM'), ('15:45', '3:45 PM'), ('16:00', '4:00 PM'), ('16:15', '4:15 PM'), ('16:30', '4:30 PM'), ('16:45', '4:45 PM'), ('17:00', '5:00 PM'), ('17:15', '5:15 PM'), ('17:30', '5:30 PM'), ('17:45', '5:45 PM'), ('18:00', '6:00 PM'), ('18:15', '6:15 PM'), ('18:30', '6:30 PM'), ('18:45', '6:45 PM'), ('19:00', '7:00 PM'), ('19:15', '7:15 PM'), ('19:30', '7:30 PM'), ('19:45', '7:45 PM'), ('20:00', '8:00 PM'), ('20:15', '8:15 PM'), ('20:30', '8:30 PM'), ('20:45', '8:45 PM'), ('21:00', '9:00 PM'), ('21:15', '9:15 PM'), ('21:30', '9:30 PM'), ('21:45', '9:45 PM'), ('22:00', '10:00 PM'), ('22:15', '10:15 PM'), ('22:30', '10:30 PM'), ('22:45', '10:45 PM'), ('23:00', '11:00 PM'), ('23:15', '11:15 PM'), ('23:30', '11:30 PM'), ('23:45', '11:45 PM')], default='12:00', max_length=5),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='collect_time_start',
            field=models.CharField(choices=[('11:00', '11:00 AM'), ('11:15', '11:15 AM'), ('11:30', '11:30 AM'), ('11:45', '11:45 AM'), ('12:00', '12:00 PM'), ('12:15', '12:15 PM'), ('12:30', '12:30 PM'), ('12:45', '12:45 PM'), ('13:00', '1:00 PM'), ('13:15', '1:15 PM'), ('13:30', '1:30 PM'), ('13:45', '1:45 PM'), ('14:00', '2:00 PM'), ('14:15', '2:15 PM'), ('14:30', '2:30 PM'), ('14:45', '2:45 PM'), ('15:00', '3:00 PM'), ('15:15', '3:15 PM'), ('15:30', '3:30 PM'), ('15:45', '3:45 PM'), ('16:00', '4:00 PM'), ('16:15', '4:15 PM'), ('16:30', '4:30 PM'), ('16:45', '4:45 PM'), ('17:00', '5:00 PM'), ('17:15', '5:15 PM'), ('17:30', '5:30 PM'), ('17:45', '5:45 PM'), ('18:00', '6:00 PM'), ('18:15', '6:15 PM'), ('18:30', '6:30 PM'), ('18:45', '6:45 PM'), ('19:00', '7:00 PM'), ('19:15', '7:15 PM'), ('19:30', '7:30 PM'), ('19:45', '7:45 PM'), ('20:00', '8:00 PM'), ('20:15', '8:15 PM'), ('20:30', '8:30 PM'), ('20:45', '8:45 PM'), ('21:00', '9:00 PM'), ('21:15', '9:15 PM'), ('21:30', '9:30 PM'), ('21:45', '9:45 PM'), ('22:00', '10:00 PM'), ('22:15', '10:15 PM'), ('22:30', '10:30 PM'), ('22:45', '10:45 PM'), ('23:00', '11:00 PM'), ('23:15', '11:15 PM'), ('23:30', '11:30 PM'), ('23:45', '11:45 PM')], default='11:00', max_length=5),
        ),
    ]
