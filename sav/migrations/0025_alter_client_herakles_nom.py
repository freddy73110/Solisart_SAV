# Generated by Django 4.1 on 2023-06-26 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0024_client_herakles_alter_bl_herakles_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client_herakles',
            name='Nom',
            field=models.CharField(blank=True, help_text='Appuyer sur Ctrl pour sélectionner plusieurs Client', max_length=60, null=True, verbose_name='Nom'),
        ),
    ]