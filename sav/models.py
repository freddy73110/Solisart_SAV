import base64
import os
import sys
from datetime import datetime, timedelta
from django.utils import timezone
from io import BytesIO

import django.db.models
from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.functions import Lower, Substr
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator

from django.contrib.auth.models import User
from django.http import HttpResponse

from django.db.models import F, Value, Subquery, OuterRef, When, Case, CharField, TextField
from django.db.models.functions import StrIndex

from django.db.models.functions import Length
TextField.register_lookup(Length, 'length')

from Solisart_SAV import settings


def get_first_name(self):
    return self.first_name[0:1].upper() + self.first_name[1:].lower() + ' ' + self.last_name[0:1].upper() + self.last_name[1:].lower()

User.add_to_class("__str__", get_first_name)

def icon4email(self):
    profils = acces.objects.filter(utilisateur=self).order_by('profil_type').values_list('profil_type__name',
                                                                                              flat=True).distinct()
    icon = ''
    if 'Administrateur' in profils:
        icon += '&#129332; '
    if 'Technicien' in profils:
        icon += '&#128736; '
    if 'Installateur' in profils:
        icon += '&#128295; '
    if 'Propriétaire' in profils:
        icon += '&#127968; '
    return icon

User.add_to_class("icon4email", icon4email)

def validate_file_extension_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError(u'Error message')

class Fichiers(models.Model):
    titre = models.CharField(max_length=255, blank=True)
    fichier = models.FileField(upload_to='files/',max_length=300)
    telecharge_a = models.DateTimeField(auto_now_add=True)

    def extension(self):
        name, extension = os.path.splitext(self.fichier.name)
        return extension

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.titre:
            self.titre = str(self.filename())
        super(Fichiers, self).save(force_insert, force_update, using, update_fields)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.fichier.path):
            os.remove(self.fichier.path)
        super(Fichiers, self).delete(*args, **kwargs)

    def filename(self):
        return os.path.basename(self.fichier.name)

    def icon(self):
        name, extension = os.path.splitext(self.fichier.name)
        if extension == '.pdf':
            return '<i class="far fa-file-pdf"></i>'
        if extension == '.doc':
            return '<i class="far fa-file-word"></i>'
        if extension == '.zip':
            return '<i class="far fa-file-archive"></i>'
        if extension == '.ppt' or extension == '.pptx':
            return '<i class="far fa-file-powerpoint"></i>'
        if extension == '.xls' or extension == '.xlsx':
            return '<i class="far fa-file-excel"></i>'
        if extension == '.csv':
            return '<i class="fas fa-file-csv"></i>'
        if extension == '.jpg' or extension == '.png' or extension == '.PNG' or extension == '.jpeg':
            return '<i class="far fa-file-image"></i>'
        if extension == '.deb' or extension == '.exe':
            return '<i class="far fa-file-code"></i>'
        return '<span class="fa-layers fa-fw"><i class="far fa-file"></i>'\
                '<span class="fa-layers-text" data-fa-transform="shrink-11.5 down-2" style="font-weight:600">' +extension.replace('.', '')+'</span>'\
                '</span>'

    def __str__(self):
        return self.titre

class profil_user(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profil_user')
    idsa = models.CharField(max_length=50, verbose_name='id solisart')
    PW = models.CharField(max_length=50, verbose_name='mot de passe my.solisart', default='solaire')
    telephone1 = models.CharField(max_length=50, verbose_name='téléphone 1', blank=True, null=True)
    telephone2 = models.CharField(max_length=50, verbose_name='téléphone 2', blank=True, null=True)
    voie1 = models.CharField(max_length=50, verbose_name='voie 1', blank=True, null=True)
    voie2 = models.CharField(max_length=50, verbose_name='voie 2', blank=True, null=True)
    voie3 = models.CharField(max_length=50, verbose_name='voie 3', blank=True, null=True)
    codepostal = models.CharField(max_length=50, verbose_name='Code postal', blank=True, null=True)
    commune = models.CharField(max_length=50, verbose_name='Commune', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    entreprise = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='entreprise')
    departement = models.JSONField(verbose_name="liste de département", blank=True, null=True, help_text='la liste doit être du format:["XX", "XX", ...], mettre 100 pour la Belgique')
    color = models.CharField(verbose_name="couleur sur la carte", blank=True, null=True, default="#000000", max_length=10)
    mailOcommercial = models.BooleanField(default=True, verbose_name="Recevoir rapport des tickets hebdomadaires ")
    Client_herakles = models.ForeignKey("Client_herakles", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def as_dict(self):
        return {
            "idsa": self.idsa,
            "user": self.get_full_name(),
            "telephone1": self.telephone1,
            "departement": self.departement,
            "color": self.color
        }

    def get_full_name(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def icon(self):
        profils = acces.objects.filter(utilisateur=self.user).order_by('profil_type').values_list('profil_type__name', flat=True).distinct()
        icon=''
        if 'Administrateur' in profils:
            icon += '<i class="fas fa-users-cog m-1"></i>'
        if 'Technicien' in profils:
            icon += '<i class="fas fa-screwdriver m-1"></i>'
        if 'Installateur' in profils:
            icon += '<i class="fas fa-tools m-1" ></i>'
        if 'Propriétaire' in profils:
            icon += '<i class="fas fa-house-user m-1"></i>'
        return icon

    def icon4email(self):
        profils = acces.objects.filter(utilisateur=self.user).order_by('profil_type').values_list('profil_type__name',
                                                                                                  flat=True).distinct()
        icon = ''
        if 'Administrateur' in profils:
            icon += '&#129332; '
        if 'Technicien' in profils:
            icon += '&#128736; '
        if 'Installateur' in profils:
            icon += '&#128295; '
        if 'Propriétaire' in profils:
            icon += '&#127968; '
        return icon

    def installations(self):
        return installation.objects.filter(acces__utilisateur=self.user).distinct()

    def ticket(self):
        return ticket.objects.filter(utilisateur=self.user)

    def ticket_count(self):
        return ticket.objects.filter(utilisateur=self.user).count()

    def ticket_open_count(self):
        return ticket.objects.filter(utilisateur=self.user).exclude(etat=3).count()

    def commercial_ticket(self, duree=None):
        if not duree:
            duree = 15
        try:
            tickets = ticket.objects.filter(
                evenement__date__gte=timezone.today() - timedelta(days=duree),
                evenement__installation__attribut_valeur__attribut_def__description="Code postal",
            ).order_by('-evenement__date').annotate(
                instal_id=Subquery(installation.objects.filter(evenement__ticket__id=OuterRef("id")).values("id")[:1]),
                num_departement1=Subquery(
                    attribut_valeur.objects.filter(
                        installation__pk=OuterRef("instal_id"),
                        attribut_def__description="Code postal").values('valeur')[:1]
                    ),
                num_departement2 = Substr('num_departement1', 1, 2),
                num_departement=Case(
                    When(num_departement1__length=4, then=Value(str(100))),
                    When(num_departement1__length=5, then='num_departement2'),
                    output_field=CharField()
                )
            ).filter(
                num_departement__in=list(self.departement))
            return tickets
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            return None

    def commercial_ticket_open(self, duree=None):
        if self.commercial_ticket(duree=duree):
            return self.commercial_ticket(duree=duree).exclude(etat=3)
        else:
            return None

    def geolocalisation(self):
        if self.latitude and self.longitude:
            return [float(str(self.latitude).replace(',', '.')), float(str(self.longitude).replace(',', '.'))]
        else:
            None


    @receiver(post_save, sender=User)
    def create_user_profil(sender, instance, created, **kwargs):
        if created:
            profil_user.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profil_user.save()

    class Meta:
        app_label = 'sav'
        ordering = ['idsa']

class profil_type(models.Model):

    PROFIL_TYPE = (
        ("admin", "admin"),
        ("client", "client")
    )

    name = models.CharField(max_length=50, verbose_name='Nom')
    type = models.CharField(max_length=50, choices=PROFIL_TYPE, verbose_name='Type')
    idsa = models.IntegerField(verbose_name='id solisart')

    def __str__(self):
        return str(self.type) + ' ' + str(self.name)

class installation(models.Model):
    TYPE_COMMUNICATION=(
        (0, "Carte de régulation sans échange de données"),
        (1, ""),
        (2, "Carte de régulation avec échange de données"),
        (3, "..."),
        (4, "Carte de régulation NG avec nano-serveur v3")
    )
    idsa = models.CharField(max_length=50, verbose_name='id solisart')
    type_communication = models.IntegerField(verbose_name="Type de communication", choices=TYPE_COMMUNICATION, blank=True, null=True)
    version_carte_firmware = models.CharField(max_length=20, verbose_name='Version de carte Firmware', blank=True, null=True)
    version_carte_interface = models.CharField(max_length=20, verbose_name='Version de carte Interface', blank=True, null=True)
    version_serveur_appli = models.CharField(max_length=20, verbose_name='Version de carte Application', blank=True, null=True)
    adresse_ip_wan = models.CharField(max_length=20, verbose_name='Adresse IP WAN', blank=True, null=True)
    port_tcp_wan = models.IntegerField(verbose_name='Port TCP WAN', blank=True, null=True)
    schema_installation = models.FileField(verbose_name="Schéma de principe",
                                           upload_to='Schema_installation/',
                                           validators=[validate_file_extension_pdf],
                                           null=True, blank=True)

    def __str__(self):
        text = self.idsa + ' / ' +str(self.proprio()) if self.proprio() else self.idsa
        text+= " (" + str(self.departement()) +')' if self.departement() else ''
        return text

    def MES_count(self):
        return MES.objects.filter(evenement__installation=self).distinct().count()

    def ticket_count(self):
        return ticket.objects.filter(evenement__installation=self).distinct().count()

    def ticket_open_count(self):
        return ticket.objects.filter(evenement__installation=self).distinct().exclude(etat=3).count()

    def histo(self):
        try:
            return [str(i) for i in historique.objects.filter(installation=self)] if historique.objects.filter(installation=self) else None
        except Exception as ex:
            return None

    def schema(self):
        histo = self.histo()
        background = Image.open("sav/static/sav/schema_elements/Fond de schema.png")
        foreground = Image.open("sav/static/sav/schema_elements/CAPT 1 champ capteurs.png")
        background.paste(foreground, (-4, -4), foreground)
        if "Zone 1: Plancher" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C1 plancher chauffant.png")
            background.paste(foreground, (882, 372), foreground)
        if "Zone 1: Radiateur" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C1 radiateurs.png")
            background.paste(foreground, (882, 372), foreground)
        if "Zone 2: Radiateur" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C2 radiateurs.png")
            background.paste(foreground, (838, 240), foreground)
        if "Zone 2: Plancher" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C2 plancher chauffant.png")
            background.paste(foreground, (841, 240), foreground)
        if "Zone 2: Piscine" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C2 piscine.png")
            background.paste(foreground, (841, 240), foreground)
        if "Zone 3: Radiateur" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C3 radiateurs.png")
            background.paste(foreground, (795, 100), foreground)
        if "Zone 3: Plancher" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C3 plancher chauffant.png")
            background.paste(foreground, (795, 100), foreground)
        if "Zone 3: Piscine" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C3 Piscine.png")
            background.paste(foreground, (790, 100), foreground)
        if "Zone 4: Plancher" in histo:
            foreground = Image.open("sav/static/sav/schema_elements/C7 plancher chauffant.png")
            background.paste(foreground, (707, 86), foreground)
        if "Type ballon sanitaire: un" in histo or "Type ballon sanitaire: soleil et appoint" in histo:
            img = Image.open("sav/static/sav/schema_elements/BAL ballon ECS 2 échangeurs.png")
            basewidth = 647
            wpercent = (basewidth / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(wpercent)))
            img = img.resize((basewidth, hsize), Image.ANTIALIAS)
            background.paste(img, (130, 58 ), img)
        if "Appoint1: Electrique" in histo or "Appoint1: Chaudière" in histo:
            img = Image.open("sav/static/sav/schema_elements/APP AUT appoint simple.png")
            background.paste(img, (470, 65 ), img)
        if "Appoint1: Pompe à Chaleur" in histo or "Appoint1: Chaudière condensation" in histo:
            img = Image.open("sav/static/sav/schema_elements/APP PAC appoint sur casse pression.png")
            background.paste(img, (470, 71  ), img)
        if "Appoint1: Bois granulés sur T16" in histo:
            img = Image.open(
                "sav/static/sav/schema_elements/APP GRA appoint sur échangeur T16.png")
            background.paste(img, (470, 71), img)
        if "Appoint2: Bois granulés sur T16" in histo:
            img = Image.open(
                "sav/static/sav/schema_elements/APP GRA Appoint sur casse pression T16.png")
            background.paste(img, (470, 71), img)
        if "Appoint2: Bois" in histo:
            img = Image.open("sav/static/sav/schema_elements/C7 appoint bois.png")
            background.paste(img, (690, 71  ), img)
        if "Type ballon tampon: avec ballon tampon" in histo:
            img = Image.open("sav/static/sav/schema_elements/BT ballon tampon avec échangeur.png")
            background.paste(img, (180, 55 ), img)
            img2 = Image.open("sav/static/sav/schema_elements/Circulateur C6.png")
            background.paste(img2, (69, 417), img2)

        thumb_io = BytesIO()
        background.save(thumb_io, format='png')
        return base64.b64encode(thumb_io.getvalue()).decode('utf-8')

    def user_acces(self):
        return acces.objects.filter(installation=self)

    def proprio(self):
        try:
            return User.objects.get(acces__installation=self, acces__profil_type__name="Propriétaire")
        except:
            return None

    def installateur(self):
        try:
            return User.objects.get(acces__installation=self, acces__profil_type__name="Installateur")
        except:
            return None

    def coordonnee_GPS(self):
        try:
            a = attribut_valeur.objects.get(installation=self,
                                            attribut_def__description="Coordonnées GPS DD")
            return a
        except:
            return ''

    def departement(self):
        try:
            CP = attribut_valeur.objects.get(installation=self,
                                    attribut_def__description="Code postal").valeur
            if len(CP)==5:
                return CP[0:2]
            elif len(CP)==4:
                return 100
            else:
                None
        except:
            return None

    def ticketencours(self):
        return ticket.objects.filter(evenement__installation=self).exclude(etat=2).count()

    class Meta:
        app_label = 'sav'
        ordering = ['idsa']

class acces(models.Model):

    utilisateur=models.ForeignKey(User, verbose_name='Utilisateur', on_delete=models.CASCADE)
    profil_type=models.ForeignKey(profil_type, verbose_name='Type de Profil', on_delete=models.CASCADE)
    installation=models.ForeignKey(installation, verbose_name='Installation', on_delete=models.CASCADE)

class attribut_def(models.Model):

    description = models.CharField(max_length=100, verbose_name='Description')
    idsa = models.IntegerField(verbose_name='id solisart')

    def __str__(self):
        return str(self.description)

class attribut_valeur(models.Model):
    installation = models.ForeignKey(installation, verbose_name='Installation', on_delete=models.CASCADE)
    attribut_def = models.ForeignKey(attribut_def, verbose_name='Attribut définition', on_delete=models.CASCADE)
    valeur = models.TextField(max_length=1500, verbose_name='Valeur')

    def __str__(self):
        return str(self.attribut_def) + ': ' + str(self.valeur)

class solution(models.Model):
    solution = models.CharField(max_length=100, verbose_name="Solution")

    def __str__(self):
        return str(self.solution)

    class Meta:
        ordering = ['solution']

class type_cause(models.IntegerChoices):
    CONNEXION = 0, 'Connexion'
    ELECTRONIQUE = 1, 'Electronique'
    MODULE = 2, 'Module'
    APPOINT = 3, 'Appoint'
    BALLON = 4, 'Ballon'
    CAPTEUR = 5, 'Capteur'
    PROD = 6, 'Problème en Production'
    UTILISATION = 7, 'Utilisation'


class cause(models.Model):
    categorie = models.IntegerField(default=type_cause.CONNEXION, choices=type_cause.choices, verbose_name="Catégorie")
    sous_categorie = models.CharField(max_length=100, verbose_name="Sous catégorie")
    solution = models.ManyToManyField('solution', null=True, blank=True, verbose_name='Solutions')

    def __str__(self):
        return str(type_cause(self.categorie).label) + ' - ' + str(self.sous_categorie)

    class Meta:
        ordering = ['categorie', 'sous_categorie']

class type_probleme(models.IntegerChoices):
    CONNEXION = 0, 'Pas de Connexion'
    PBTECH = 1, 'Problème technique'
    PIECESSAV = 2, 'Pièces SAV'
    HELP = 3, 'Aide au paramétrage'
    INFO = 4, 'Information diverse'
    PRESTA = 5, 'Demande de prestation'
    ERROR_PROD = 6, 'Erreur de production'
    PREVENTIF = 7, 'Préventif'

class probleme(models.Model):
    categorie = models.IntegerField(default=type_probleme.CONNEXION, choices=type_probleme.choices, verbose_name="Catégorie")
    sous_categorie = models.CharField(max_length=100, verbose_name="Sous catégorie")
    causes = models.ManyToManyField('cause', null=True, blank=True,verbose_name='Causes possible')

    def __str__(self):
        return str(type_probleme(self.categorie).label) + ' - ' + str(self.sous_categorie)

    class Meta:
        ordering = ['categorie', 'sous_categorie']

class forme_contact(models.IntegerChoices):
    TELEPHONE = 0, 'Téléphone'
    EMAIL = 1, 'Email'
    PHYSIQUEMENT = 2, 'Physiquement'
    AUCUN = 3, 'Aucun'

class etat(models.IntegerChoices):
    OUVERTURE = 0, 'Ouverture'
    ENCOURS = 1, 'En cours'
    ARAPPELER = 2, 'A rappeler'
    CLOTURE = 3, 'Clôturé'

class evenement(models.Model):
    date = models.DateTimeField(verbose_name='Date', help_text="Date et heure de événement", default=datetime.now())
    technicien_sav = models.ForeignKey(User, verbose_name='technicien sav', on_delete=models.CASCADE)
    installation = models.ForeignKey(installation, verbose_name='Installation', on_delete=models.CASCADE)

    def ticket(self):
        try:
            return ticket.objects.get(evenement=self)
        except:
            return None

    def MES(self):
        try:
            return MES.objects.get(evenement=self)
        except:
            return None

    def icon(self):
        if self.forme == 0:
            return '<i class="fas fa-phone-alt"></i>'
        elif self.forme == 1:
            return '<i class="fas fa-at"></i>'
        else:
            return '<i class="fas fa-people-arrows"></i>'

    def duree(self):
        return timezone.now()

    def __str__(self):
        return str(self.date) + ' ' + str(self.installation)

class MES(models.Model):
    evenement = models.ForeignKey('evenement', verbose_name='Evenement', on_delete=models.CASCADE, null=True, blank=True)
    detail = models.TextField(verbose_name="Détail", null=True, blank=True)
    fichier = models.ManyToManyField('Fichiers', verbose_name="Fichiers", null=True, blank=True)

    def icon_technicien_sav(self):
        try:

            initial=(self.evenement.technicien_sav.first_name[0] + self.evenement.technicien_sav.last_name[0]).upper()
        except:
            initial = 'Inconnu'

        html='<div class="fa-2x">\
                              <span class="fa-layers fa-fw">\
                                  <i class="fas fa-user-md"></i>\
                                  <span class="fa-layers-text badge rounded-pill bg-danger" data-fa-transform="shrink-10 up-10 right-12 grow-2" style="{background:Tomato}">'+initial+'</span>\
                                </span>\
                              </div>'
        return html



# class CL_herakles(models.Model):
#     CL = models.CharField(verbose_name="Commande", max_length=25, help_text="Appuyer sur Ctrl pour sélectionner plusieurs commande")
#
#     def __str__(self):
#         return str(self.CL)
#
#     class Meta:
#         ordering = ("-CL",)

class devis_herakles(models.Model):
    devis = models.CharField(verbose_name="Devis", max_length=25, help_text="Appuyer sur Ctrl pour sélectionner plusieurs devis")

    def __str__(self):
        return str(self.devis)

    class Meta:
        ordering = ("-devis",)

class BL_herakles(models.Model):
    BL = models.CharField(verbose_name="BL", max_length=25, help_text="Appuyer sur Ctrl pour sélectionner plusieurs BL")

    def __str__(self):
        return str(self.BL)

    class Meta:
        ordering = ("-BL",)

class client_herakles(models.Model):
    Code_Client = models.CharField(verbose_name="Code Client", max_length=25, help_text="Appuyer sur Ctrl pour sélectionner plusieurs Client")
    Nom = models.CharField(verbose_name="Nom", max_length=60, null=True, blank=True, help_text="Appuyer sur Ctrl pour sélectionner plusieurs Client")

    def __str__(self):
        return str(self.Code_Client)

    class Meta:
        ordering = ("Code_Client",)

class ticket(models.Model):
    evenement = models.ForeignKey('evenement', verbose_name='Evenement', on_delete=models.CASCADE, null=True, blank=True)
    forme = models.IntegerField(default=forme_contact.TELEPHONE, choices=forme_contact.choices, verbose_name='Forme')
    etat = models.IntegerField(default=etat.OUVERTURE, choices=etat.choices, verbose_name='Etat')
    utilisateur = models.ForeignKey(User, verbose_name='Contact', on_delete=models.CASCADE)
    probleme = models.ForeignKey(probleme, verbose_name='Symptômes', on_delete=models.CASCADE)
    cause = models.ForeignKey(cause, verbose_name='Causes', on_delete=models.CASCADE, null=True, blank=True)
    detail = models.TextField(verbose_name="Détail", null=True, blank=True)
    devis = models.ManyToManyField('devis_herakles', null=True, blank=True)
    BL = models.ManyToManyField('BL_herakles', null=True, blank=True)
    fichier = models.ManyToManyField('Fichiers', verbose_name="Fichiers", null=True, blank=True)

    def as_dict(self):
        return {
            "id": self.id,
            "date": self.evenement.date.strftime('%d/%m/%Y %H:%M'),
            "installation":str(self.evenement.installation),
            "installation_link": '<a href="/installation/' + str(self.evenement.installation.id) + '">'+ str(self.evenement.installation) + '</a>',
            "forme": str(self.icon_forme()) + ' ' + str(forme_contact(self.forme).name),
            "etat": str(self.icon_etat()) + ' ' + str(etat(self.etat).name),
            "installeur": str(self.utilisateur),
            "installateur_link": '<a href="/utilisateur/' + str(self.utilisateur.id) + '">'+ str(self.utilisateur) + '</a>',
            "probleme": str(self.probleme),
            "cause": str(self.cause) if self.cause else '',
            "detail": str(self.detail),
            "fichier": [f.titre for f in self.fichier.all()]
        }

    def icon_technicien_sav(self):
        try:

            initial=(self.evenement.technicien_sav.first_name[0] + self.evenement.technicien_sav.last_name[0]).upper()
        except:
            initial = 'Inconnu'

        html='<div class="fa-2x">\
                              <span class="fa-layers fa-fw">\
                                  <i class="fas fa-user-md"></i>\
                                  <span class="fa-layers-text badge rounded-pill bg-danger" data-fa-transform="shrink-10 up-10 right-12 grow-2" style="{background:Tomato}">'+initial+'</span>\
                                </span>\
                              </div>'
        return html
    def icon_etat(self):
        if self.etat == 0:
            return '<i class="fas fa-play"></i>'
        if self.etat == 1:
            return '<i class="fas fa-pause"></i>'
        if self.etat == 2:
            return '<i class="far fa-comment"></i>'
        if self.etat == 3:
            return '<i class="fas fa-stop"></i>'
    def icon_forme(self):
        if self.forme == 0:
            return '<i class="fas fa-phone-alt"></i>'
        if self.forme ==1:
            return '<i class="fas fa-at"></i>'
        if self.forme ==2:
            return '<i class="fas fa-comments"></i>'
        if self.forme ==3:
            return '<i class="fas fa-exclamation-triangle"></i>'

    def __str__(self):
        try:
            strl=str(self.evenement) + ' ' + str(etat(self.etat).name) + ' ' + str(self.probleme)
            if self.cause:
                strl+= " - " + str(self.cause)
            return strl

        except:
            return str(self.evenement) + ' ' + str(etat(self.etat).name)

class donnee(models.Model):
    idsa = models.CharField(max_length=50, verbose_name='id solisart')
    nom_carte = models.CharField(max_length=50, verbose_name="Nom carte")
    description = models.CharField(max_length=100, verbose_name="Description")

    def __str__(self):
        return str(self.nom_carte)

class historique(models.Model):
    installation = models.ForeignKey(installation, verbose_name='Installation', on_delete=models.CASCADE)
    heure = models.DateTimeField(verbose_name="Date et heure", null=True, blank=True )
    donnee = models.ForeignKey(donnee, verbose_name='Donnée', on_delete=models.CASCADE)
    valeur = models.CharField(max_length=50, verbose_name='Valeur')

    def __str__(self):
        try:
            if str(self.donnee) == "Type_Ballon_C":
                if int(self.valeur) == 0:
                    return "Type ballon tampon: sans ballon tampon"
                elif int(self.valeur) == 1:
                    return "Type ballon tampon: avec ballon tampon"
            elif str(self.donnee) == "Type_Ballon_S":
                if int(self.valeur) == 0:
                    return "Type ballon sanitaire: un"
                elif int(self.valeur) == 1:
                    return "Type ballon sanitaire: soleil et appoint"
            elif "Type_Appoint" in str(self.donnee):
                TA = "Appoint1" if "(0)" in str(self.donnee) else "Appoint2"
                if int(self.valeur) == 0:
                    TA+= ': ' + 'aucun'
                elif int(self.valeur) == 1:
                    TA+= ': ' + 'Chaudière'
                elif int(self.valeur) == 2:
                    TA+= ': ' + 'Chaudière condensation'
                elif int(self.valeur) == 3:
                    TA+= ': ' + 'Electrique'
                elif int(self.valeur) == 4:
                    TA+= ': ' + 'Pompe à Chaleur'
                elif int(self.valeur) == 5:
                    TA+= ': ' + 'Bois granulés sur T16'
                elif int(self.valeur) == 6:
                    TA+= ': ' + 'Bois'
                return TA
            elif "Type_Emetteur" in str(self.donnee):
                TE = "Zone " + str(int(str(self.donnee).replace('Type_Emetteur(','').replace(')', '')) +1)
                if int(self.valeur) == 0:
                    TE += ': aucun'
                elif int(self.valeur) == 1:
                    TE += ': Plancher'
                elif int(self.valeur) == 2:
                    TE += ': Radiateur'
                elif int(self.valeur) == 3:
                    TE += ': Piscine'
                elif int(self.valeur) == 4:
                    TE += ': Ventilo-convecteur'
                elif int(self.valeur) == 5:
                    TE += ': Décharge capteur'
                elif int(self.valeur) == 6:
                    TE += ': Radiateur en réhausse'
                return TE
            else:
                return str(self.donnee) + ' - ' + str(self.valeur)
        except Exception as ex:
            return 'error'

class etat_document(models.IntegerChoices):

    VALIDE = 0, 'Valide'
    OBSOLETE = 1, 'Obsolète'
    AREFONDRE = 2, 'A refondre'

class dossier(models.IntegerChoices):

    CAP = 0, 'Capteur'
    MOD = 1, 'Module'
    LOG = 2, 'Logiciel'
    ENS= 3, 'Ensemble'

class sous_dossier(models.IntegerChoices):

    INTERNE = 0, 'Interne'
    EXTERNE = 1, 'Externe'

class fichier_categorie(models.IntegerChoices):

    PS = 0, 'Processus'
    PD = 1, 'Procédure'
    MO = 2, 'Mode opératoire'
    MU = 3, "Manuel d'utilisation"

class classification(models.Model):

    categorie=models.IntegerField(default=fichier_categorie.MO, choices=fichier_categorie.choices, verbose_name='Catégorie')
    dossier=models.IntegerField(default=dossier.MOD, choices=dossier.choices, verbose_name='Dossier')
    sous_dossier=models.IntegerField(default=sous_dossier.INTERNE, choices=sous_dossier.choices, verbose_name='Interne-Externe')
    titre=models.CharField(verbose_name='Titre de la procédure', max_length=100)

    class Meta:
        app_label = 'sav'
        ordering = ['categorie', 'dossier', 'titre']

    def sigle(self):
        return "{}-{}-{}".format(
        str(fichier_categorie(self.categorie).name),
        str(dossier(self.dossier).name),
        str(sous_dossier(self.sous_dossier).name)
    )

    def sigle_toutelettre(self):
        return "{} - {}".format(
            str(fichier_categorie(self.categorie).label),
            str(dossier(self.dossier).label)
        )

    def __str__(self):
        return self.sigle() +' ' +str(self.titre)



def group_based_upload_to(instance, filename):

    return "documentation/{}".format(
        filename
    )

class documentation(models.Model):

    fichier = models.FileField(upload_to=group_based_upload_to, verbose_name="Fichier", validators=[FileExtensionValidator(allowed_extensions=["doc","docx", "pdf", "mp4", "mpeg", "avi", "wav"])])
    version = models.CharField(verbose_name="Version du document", max_length=10)
    date = models.DateField(verbose_name="Date de mise en application")
    classification = models.ForeignKey(classification, verbose_name="Classification du document", on_delete=models.CASCADE, null=True, blank=True)
    etat = models.IntegerField(default=etat_document.VALIDE, choices=etat_document.choices, verbose_name='Etat du document')
    commentaire =models.TextField(verbose_name="Commentaire évolution", max_length=500, null=True, blank=True)
    a_ameliorer=models.TextField(verbose_name="Point à améliorer", max_length=500, null=True, blank=True)

    def icon(self):
        name, extension = os.path.splitext(self.fichier.name)
        if extension == '.pdf':
            return '<i class="far fa-file-pdf"></i>'
        if extension == '.doc':
            return '<i class="far fa-file-word"></i>'
        if extension == '.zip':
            return '<i class="far fa-file-archive"></i>'
        if extension == '.ppt' or extension == '.pptx':
            return '<i class="far fa-file-powerpoint"></i>'
        if extension == '.xls' or extension == '.xlsx':
            return '<i class="far fa-file-excel"></i>'
        if extension == '.csv':
            return '<i class="fas fa-file-csv"></i>'
        if extension == '.jpg' or extension == '.png' or extension == '.PNG' or extension == '.jpeg':
            return '<i class="far fa-file-image"></i>'
        if extension == '.deb' or extension == '.exe':
            return '<i class="far fa-file-code"></i>'
        if extension =='.mp4' or extension =="mpeg" or extension == "avi" or extension =="wav":
            return '<i class="far fa-file-video"></i>'
        return '<span class="fa-layers fa-fw"><i class="far fa-file"></i>'\
                '<span class="fa-layers-text" data-fa-transform="shrink-11.5 down-2" style="font-weight:600">' +extension.replace('.', '')+'</span>'\
                '</span>'

    def extensionfile(self):
        name, extension = os.path.splitext(self.fichier.name)
        return str(extension)[1:]

    def sigle(self):
        return self.classification.sigle()

    def __str__(self):
        return  str(self.classification) + ' version ' +str(self.version) + ' ' + str(self.extensionfile())

    def validite(self):
        i = 0
        docs = documentation.objects.filter(classification=self.classification).\
                annotate(split=StrIndex(F('fichier'), Value('.')))\
                .annotate(extension=Substr(F('fichier'), F('split')+1))\
                .order_by('extension','date')
        for doc in docs:
            i+=1
            if doc == self:
                try:
                    if doc.extensionfile()==docs[i].extensionfile():
                        return docs[i].date
                        break
                    else:
                        return timezone.now().date()
                        break
                except:
                    return timezone.now().date()

    class Meta:
         app_label = 'sav'
         ordering = ['date']


class module(models.Model):

    type = models.CharField(verbose_name="Type", max_length=50)

    def __str__(self):
        return self.type
class capteur(models.Model):

    type = models.CharField(verbose_name="Capteur", max_length=50)

    def __str__(self):
        return self.type

class transporteur(models.Model):

    nom = models.CharField(verbose_name="Transporteur", max_length=50)

    def __str__(self):
        return self.nom

class CL_herakles(models.Model):
    CL = models.CharField(verbose_name="CL", max_length=25, default="default")
    BL = models.ForeignKey("BL_herakles", on_delete=models.CASCADE, null=True, blank=True)
    installateur = models.ForeignKey("client_herakles", verbose_name="installateur", on_delete=models.CASCADE, null=True, blank=True)
    information = models.TextField(verbose_name="Information", null=True, blank=True)
    date_last_update_information = models.DateField(verbose_name="Date de dernière modif commentaire", default=timezone.now())
    module = models.ForeignKey("module", on_delete=models.CASCADE, null=True, blank=True)
    capteur = models.ForeignKey("capteur", on_delete=models.CASCADE, null=True, blank=True)
    capteur_nbre = models.IntegerField(verbose_name="Nombre de capteur", default=0)
    ballon = models.CharField(verbose_name="Ballon", max_length=100, null=True, blank=True)
    transporteur = models.ForeignKey("transporteur", on_delete=models.CASCADE, null=True, blank=True)
    prix_transport = models.FloatField(verbose_name="Tarif réel du transport", default=0)
    date_livraison_prevu = models.DateField(verbose_name="Date de réception prévue", help_text='Définit sur Héraklès', null=True, blank=True)
    date_livraison = models.DateField(verbose_name="Date de livraison", help_text='Date réelle', null=True, blank=True)
    date_capteur = models.DateField(verbose_name="Date Capteur prêt", help_text='Date réelle', null=True, blank=True)
    date_capteur_prevu = models.DateField(verbose_name="Date prévu de prépa capteurs", help_text='Date prévisionnelle', null=True, blank=True)
    date_ballon = models.DateField(verbose_name="Date Ballon prêt", help_text='Date réelle', null=True, blank=True)
    date_ballon_prevu = models.DateField(verbose_name="Date prévu de prépades ballons",
                                          help_text='Date prévisionnelle', null=True, blank=True)
    date_montage_prevu = models.DateField(verbose_name="Date prévue de montage ", help_text='2 semaines avant livraison prévu',
                                            null=True, blank=True)
    date_montage = models.DateField(verbose_name="Date de montage", help_text='Date réelle', null=True,
                                      blank=True)
    date_prepa_carte = models.DateField(verbose_name="Date Carte prête", help_text='Date réelle', null=True,
                                  blank=True)
    date_prepa_carte_prevu = models.DateField(verbose_name="Date prévu pour la carte",
                                        help_text='Date prévisionnelle', null=True, blank=True)
    date_prepa = models.DateField(verbose_name="Date Prépa CL prête", help_text='Date réelle', null=True, blank=True)
    date_prepa_prevu = models.DateField(verbose_name="Date prévu de prépa du CL",
                                         help_text='Date prévisionnelle', null=True, blank=True)
    date_reglement = models.DateField(verbose_name="Date de réglement réelle",  null=True, blank=True)

    def __str__(self):
        return self.CL

    def as_dict(self):
        serial = {
            "CL": self.CL,
            "BL": self.BL,
        "installateur": str(self.installateur),
        "information" : self.information,
        "module": str(self.module),
        "capteur": str(self.capteur),
        "capteur_nbre": self.capteur_nbre,
        "ballon": str(self.ballon),
        "transporteur": str(self.transporteur)

        }
        for f in self._meta.fields:
            if 'date' in f.name:
                serial[f.name] = getattr(self, f.name, None).strftime("%Y-%m-%d %H:%M") if getattr(self, f.name, None) else None

        return serial

    def __init__(self, *args, **kwargs):
        super(CL_herakles, self).__init__(*args, **kwargs)
        self.old_information = self.information

    def save(self, *args, **kwargs):
        self.prix_transport = round(self.prix_transport, 2)
        if self.old_information != self.information:
            self.date_last_update_information=timezone.now()
        super(CL_herakles, self).save(*args, **kwargs)


# class emailbox(models.Model):
#
#     uid =  models.CharField(verbose_name="uid", max_length=100)
#     subject = models.CharField(verbose_name="subject", max_length=100, blank=True)
#     de = models.CharField(verbose_name="from_", max_length=100)
#     to = models.CharField(verbose_name="to", max_length=100, null=True, blank=True)
#     cc = models.CharField(verbose_name="cc", max_length=100, null=True, blank=True)
#     date = models.DateTimeField(verbose_name="date")
#     html = models.TextField(verbose_name="html", max_length=5000, null=True, blank=True)
#     text = models.TextField(verbose_name="text", max_length=5000, null=True, blank=True)
#     from_user = models.ForeignKey(User, verbose_name="Utilisateur", on_delete=models.CASCADE, null=True, blank=True)
#     from_installation = models.ManyToManyField('installation', verbose_name="installation correspondante", blank=True)
#
#
#     def from_user_function(self):
#         try:
#             return User.objects.get(email=self.de)
#         except:
#             return None
#
#     def from_installation_function(self):
#         try:
#             return installation.objects.filter(acces__utilisateur=self.from_user).distinct()
#         except Exception as e:
#             import sys
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_type, fname, exc_tb.tb_lineno)
#             print(e)
#             return None
#
#     def ticket_form(self):
#         from .forms import ticket_form
#         if self.from_user:
#             return ticket_form(utilisateur=User.objects.get(email=self.de), forme='email')
#         else:
#             return ticket_form(forme='email')
#
#     def add_evenement_form(self):
#         from .forms import add_evenement_form
#         if self.from_user:
#             return add_evenement_form(user=self.from_user, user_acces=User.objects.get(email=self.de), date=self.date)
#         else:
#             return add_evenement_form(user=self.from_user, date=self.date)
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#
#         self.from_user = self.from_user_function()
#         super(emailbox, self).save(force_insert, force_update, using, update_fields)
#
#     @receiver(post_save)
#     def affect_installation(sender, **kwargs):
#         try:
#             if not kwargs['instance'].from_installation.exists():
#                 for instal in kwargs['instance'].from_installation_function():
#                     kwargs['instance'].from_installation.add(instal)
#         except:
#             pass
#
#
#
#
# class attachement(models.Model):
#
#     email = models.ForeignKey('emailbox', verbose_name='email', on_delete=models.CASCADE)
#     filename = models.CharField(verbose_name="Filename", max_length=100)
#     content_type = models.CharField(verbose_name="Type content", max_length=100)
#     payload = models.BinaryField(verbose_name="payload", max_length=100)
#
