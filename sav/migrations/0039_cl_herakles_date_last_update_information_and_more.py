# Generated by Django 4.1 on 2023-09-05 13:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0038_cl_herakles_prix_transport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cl_herakles',
            name='date_last_update_information',
            field=models.DateField(default=datetime.datetime(2023, 9, 5, 13, 47, 30, 512008, tzinfo=datetime.timezone.utc), verbose_name='Date de dernière modif commentaire'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 5, 15, 47, 30, 507307), help_text='Date et heure de événement', verbose_name='Date'),
        ),
    ]