# Generated by Django 4.1 on 2022-12-21 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0016_profil_user_departement_alter_fichiers_fichier'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil_user',
            name='color',
            field=models.CharField(blank=True, default='#000000', max_length=10, null=True, verbose_name='couleur sur la carte'),
        ),
    ]