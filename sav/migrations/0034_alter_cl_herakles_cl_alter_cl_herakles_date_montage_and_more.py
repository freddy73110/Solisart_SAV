# Generated by Django 4.1 on 2023-08-07 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0033_transporteur_alter_evenement_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cl_herakles',
            name='CL',
            field=models.CharField(default='CL23', max_length=25, verbose_name='CL'),
        ),
        migrations.AlterField(
            model_name='cl_herakles',
            name='date_montage',
            field=models.DateField(blank=True, help_text='Définit sur Héraklès', null=True, verbose_name='Date de montage'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 7, 14, 39, 20, 356935), help_text='Date et heure de événement', verbose_name='Date'),
        ),
    ]