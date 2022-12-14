# Generated by Django 4.1 on 2022-09-01 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='attribut_def',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, verbose_name='Description')),
                ('idsa', models.IntegerField(verbose_name='id solisart')),
            ],
        ),
        migrations.CreateModel(
            name='installation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idsa', models.CharField(max_length=50, verbose_name='id solisart')),
                ('type_communication', models.IntegerField(blank=True, choices=[(0, 'Carte de régulation sans échange de données'), (1, ''), (2, 'Carte de régulation avec échange de données'), (3, '...'), (4, 'Carte de régulation NG avec nano-serveur v3')], null=True, verbose_name='Type de communication')),
                ('version_carte_firmware', models.CharField(blank=True, max_length=20, null=True, verbose_name='Version de carte Firmware')),
                ('version_carte_interface', models.CharField(blank=True, max_length=20, null=True, verbose_name='Version de carte Interface')),
                ('version_serveur_appli', models.CharField(blank=True, max_length=20, null=True, verbose_name='Version de carte Application')),
                ('adresse_ip_wan', models.CharField(blank=True, max_length=15, null=True, verbose_name='Adresse IP WAN')),
                ('port_tcp_wan', models.IntegerField(blank=True, null=True, verbose_name='POrt TCP WAN')),
            ],
        ),
        migrations.CreateModel(
            name='profil',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('idsa', models.CharField(max_length=50, verbose_name='id solisart')),
                ('PW', models.CharField(default='solaire', max_length=50, verbose_name='mot de passe my.solisart')),
                ('telephone1', models.CharField(blank=True, max_length=50, null=True, verbose_name='téléphone 1')),
                ('telephone2', models.CharField(blank=True, max_length=50, null=True, verbose_name='téléphone 2')),
                ('voie1', models.CharField(blank=True, max_length=50, null=True, verbose_name='voie 1')),
                ('voie2', models.CharField(blank=True, max_length=50, null=True, verbose_name='voie 2')),
                ('voie3', models.CharField(blank=True, max_length=50, null=True, verbose_name='voie 3')),
                ('codepostal', models.CharField(blank=True, max_length=50, null=True, verbose_name='Code postal')),
                ('commune', models.CharField(blank=True, max_length=50, null=True, verbose_name='Commune')),
            ],
        ),
        migrations.CreateModel(
            name='profil_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('type', models.CharField(choices=[('admin', 'admin'), ('client', 'client')], max_length=50, verbose_name='Type')),
                ('idsa', models.IntegerField(verbose_name='id solisart')),
            ],
        ),
        migrations.CreateModel(
            name='attribut_valeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valeur', models.CharField(max_length=100, verbose_name='Valeur')),
                ('attribut_def', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sav.attribut_def', verbose_name='Attribut définition')),
                ('installation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sav.installation', verbose_name='Installation')),
            ],
        ),
        migrations.CreateModel(
            name='acces',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('installation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sav.installation', verbose_name='Installation')),
                ('profil_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sav.profil_type', verbose_name='Type de Profil')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur')),
            ],
        ),
    ]
