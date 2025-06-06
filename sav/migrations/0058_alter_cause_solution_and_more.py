# Generated by Django 4.1 on 2024-09-03 07:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sav", "0057_assembly_detail_alter_assembly_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cause",
            name="solution",
            field=models.ManyToManyField(
                blank=True, to="sav.solution", verbose_name="Solutions"
            ),
        ),
        migrations.AlterField(
            model_name="cl_herakles",
            name="date_last_update_information",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 9, 3, 7, 34, 37, 3708, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date de dernière modif commentaire",
            ),
        ),
        migrations.AlterField(
            model_name="cl_herakles",
            name="fichier",
            field=models.ManyToManyField(
                blank=True, to="sav.fichiers", verbose_name="Fichiers"
            ),
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 9, 3, 7, 34, 37, 3708, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date d'évaluation",
            ),
        ),
        migrations.AlterField(
            model_name="evenement",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 9, 3, 9, 34, 36, 991719),
                help_text="Date et heure de événement",
                verbose_name="Date",
            ),
        ),
        migrations.AlterField(
            model_name="mes",
            name="fichier",
            field=models.ManyToManyField(
                blank=True, to="sav.fichiers", verbose_name="Fichiers"
            ),
        ),
        migrations.AlterField(
            model_name="noncompliance",
            name="fichier",
            field=models.ManyToManyField(
                blank=True, to="sav.fichiers", verbose_name="Fichiers"
            ),
        ),
        migrations.AlterField(
            model_name="probleme",
            name="causes",
            field=models.ManyToManyField(
                blank=True, to="sav.cause", verbose_name="Causes possible"
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="BL",
            field=models.ManyToManyField(blank=True, to="sav.bl_herakles"),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="devis",
            field=models.ManyToManyField(blank=True, to="sav.devis_herakles"),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="fichier",
            field=models.ManyToManyField(
                blank=True, to="sav.fichiers", verbose_name="Fichiers"
            ),
        ),
    ]
