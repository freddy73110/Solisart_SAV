# Generated by Django 4.1 on 2024-08-13 08:33

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sav", "0053_validationmodule_description_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="assembly",
            options={"ordering": ["validation__id"]},
        ),
        migrations.AddField(
            model_name="tracabiliy",
            name="location",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "C1"),
                    (1, "C2"),
                    (2, "C3"),
                    (3, "C4"),
                    (4, "C5"),
                    (5, "C6"),
                    (6, "C7"),
                    (7, "Appoint"),
                    (8, "Tampon"),
                ],
                default=0,
                null=True,
                verbose_name="Emplacement",
            ),
        ),
        migrations.AlterField(
            model_name="cl_herakles",
            name="date_last_update_information",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 13, 8, 33, 47, 896638, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date de dernière modif commentaire",
            ),
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="date",
            field=models.DateField(
                default=datetime.datetime(
                    2024, 8, 13, 8, 33, 47, 897643, tzinfo=datetime.timezone.utc
                ),
                verbose_name="Date d'évaluation",
            ),
        ),
        migrations.AlterField(
            model_name="evenement",
            name="date",
            field=models.DateTimeField(
                default=datetime.datetime(2024, 8, 13, 10, 33, 47, 892632),
                help_text="Date et heure de événement",
                verbose_name="Date",
            ),
        ),
        migrations.AlterField(
            model_name="tracability_organ",
            name="name",
            field=models.CharField(max_length=100, verbose_name="Référence Héraklès"),
        ),
        migrations.AlterField(
            model_name="tracabiliy",
            name="SN",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="Numéro de série"
            ),
        ),
        migrations.AlterField(
            model_name="tracabiliy",
            name="batch",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="batch",
                to="sav.batch",
                verbose_name="Lot",
            ),
        ),
        migrations.AlterField(
            model_name="tracabiliy",
            name="organ",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracability_organ",
                to="sav.tracability_organ",
                verbose_name="Organe",
            ),
        ),
    ]