# Generated by Django 4.1 on 2024-08-22 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sav", "0056_rename_tracabiliy_tracability_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="assembly",
            name="detail",
            field=models.TextField(
                blank=True, max_length=200, null=True, verbose_name="Description"
            ),
        ),
        migrations.AlterField(
            model_name="assembly",
            name="date",
            field=models.DateField(
                blank=True, null=True, verbose_name="Date de réalisation"
            ),
        ),
        migrations.AlterField(
            model_name="batch",
            name="comment",
            field=models.TextField(
                blank=True,
                help_text="Tests, remarques, ...",
                max_length=500,
                null=True,
                verbose_name="Commentaire",
            ),
        ),
        migrations.AlterField(
            model_name="cl_herakles",
            name="date_last_update_information",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 22, 11, 41, 29, 906667, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date de dernière modif commentaire",
            ),
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 22, 11, 41, 29, 906667, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date d'évaluation",
            ),
        ),
        migrations.AlterField(
            model_name="evenement",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 22, 13, 41, 29, 906667),
                help_text="Date et heure de événement",
                verbose_name="Date",
            ),
        ),
    ]