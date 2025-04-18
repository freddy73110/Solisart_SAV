# Generated by Django 4.1 on 2024-08-06 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("sav", "0051_batch_tracability_organ_validationmodule_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cl_herakles",
            name="date_last_update_information",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 6, 14, 1, 42, 234806, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date de dernière modif commentaire",
            ),
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 6, 14, 1, 42, 234806, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date d'évaluation",
            ),
        ),
        migrations.AlterField(
            model_name="evenement",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 6, 16, 1, 42, 234806),
                help_text="Date et heure de événement",
                verbose_name="Date",
            ),
        ),
    ]
