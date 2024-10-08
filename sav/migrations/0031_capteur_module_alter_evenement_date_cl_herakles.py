# Generated by Django 4.1 on 2023-08-04 12:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0030_alter_evenement_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='capteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(verbose_name='Capteur')),
            ],
        ),
        migrations.CreateModel(
            name='module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.TextField(verbose_name='Type')),
            ],
        ),
        migrations.AlterField(
            model_name='evenement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 4, 14, 39, 32, 722241), help_text='Date et heure de événement', verbose_name='Date'),
        ),
        migrations.CreateModel(
            name='CL_herakles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CL', models.CharField(max_length=25, verbose_name='CL')),
                ('information', models.TextField(blank=True, null=True, verbose_name='Information')),
                ('date_livraison_prevu', models.DateField(blank=True, help_text='Définit sur Héraklès', null=True, verbose_name='Date de livraison prévue')),
                ('date_livraison', models.DateField(blank=True, help_text='Définit sur Héraklès', null=True, verbose_name='Date de livraison')),
                ('date_montage_prevu', models.DateField(blank=True, help_text='Définit sur Héraklès', null=True, verbose_name='Date de livraison prévue')),
                ('date_montage', models.DateField(blank=True, help_text='Définit sur Héraklès', null=True, verbose_name='Date de livraison')),
                ('date_reglement', models.DateField(blank=True, null=True, verbose_name='Date de réglement')),
                ('capteur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sav.capteur')),
                ('installateur', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sav.client_herakles', verbose_name='installateur')),
                ('module', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sav.module')),
            ],
        ),
    ]
