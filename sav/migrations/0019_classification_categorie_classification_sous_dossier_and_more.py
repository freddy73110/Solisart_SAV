# Generated by Django 4.1 on 2023-02-24 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sav', '0018_classification_alter_profil_user_departement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='categorie',
            field=models.IntegerField(choices=[(0, 'Processus'), (1, 'Procédure'), (2, 'Mode opératoire'), (3, "Manuel d'utilisation")], default=2, verbose_name='Catégorie'),
        ),
        migrations.AddField(
            model_name='classification',
            name='sous_dossier',
            field=models.IntegerField(choices=[(0, 'Interne'), (1, 'Externe')], default=0, verbose_name='Interne-Externe'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='dossier',
            field=models.IntegerField(choices=[(0, 'Capteur'), (1, 'Module'), (2, 'Logiciel'), (3, 'Ensemble')], default=1, verbose_name='Dossier'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='titre',
            field=models.CharField(max_length=100, verbose_name='Titre de la procédure'),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='a_ameliorer',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Point à améliorer'),
        ),
        migrations.AlterField(
            model_name='documentation',
            name='commentaire',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='Commentaire évolution'),
        ),
    ]
