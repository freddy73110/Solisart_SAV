import base64
import os
from datetime import datetime, timedelta
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.db.models.functions import Lower, Substr
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.http import HttpResponse


def get_first_name(self):
    return self.first_name[0:1].upper() + self.first_name[1:].lower() + ' ' + self.last_name[0:1].upper() + self.last_name[1:].lower()

User.add_to_class("__str__", get_first_name)

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
                evenement__date__gte=datetime.today() - timedelta(days=duree),
                evenement__installation__attribut_valeur__attribut_def__description="Code postal",
            ).order_by('-evenement__date').annotate(num_departement=Lower(Substr('evenement__installation__attribut_valeur__valeur', 1, 2))).filter(
                num_departement__in=list(self.departement))
            return tickets
        except:
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
        return [str(i) for i in historique.objects.filter(installation=self)]

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
            return str(attribut_valeur.objects.get(installation=self,
                                    attribut_def__description="Code postal").valeur)[0:2]
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

class type_probleme(models.IntegerChoices):
    CONNEXION = 0, 'Pas de Connexion'
    PBTECH = 1, 'Problème technique'
    PIECESSAV = 2, 'Pièces SAV'
    HELP = 3, 'Aide au paramétrage'
    INFO = 4, 'Information diverse'
    PRESTA = 5, 'Demande de prestation'
    ERROR_PROD = 6, 'Erreur de production'

class probleme(models.Model):
    categorie = models.IntegerField(default=type_probleme.CONNEXION, choices=type_probleme.choices, verbose_name="Catégorie")
    sous_categorie = models.CharField(max_length=100, verbose_name="Sous catégorie")

    def __str__(self):
        return str(type_probleme(self.categorie).label) + ' - ' + str(self.sous_categorie)

    class Meta:
        ordering = ['categorie', 'sous_categorie']

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

    def __str__(self):
        return str(type_cause(self.categorie).label) + ' - ' + str(self.sous_categorie)

    class Meta:
        ordering = ['categorie', 'sous_categorie']

class forme_contact(models.IntegerChoices):
    TELEPHONE = 0, 'Téléphone'
    EMAIL = 1, 'Email'
    PHYSIQUEMENT = 2, 'Physiquement'

class etat(models.IntegerChoices):
    OUVERTURE = 0, 'Ouverture'
    ENCOURS = 1, 'En cours'
    ARAPPELER = 2, 'A rappeler'
    CLOTURE = 3, 'Clôturé'

class evenement(models.Model):
    date = models.DateTimeField(verbose_name='Date', help_text="Date et heure de événement", default=datetime.now)
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
        return datetime.now()

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

class ticket(models.Model):
    evenement = models.ForeignKey('evenement', verbose_name='Evenement', on_delete=models.CASCADE, null=True, blank=True)
    forme = models.IntegerField(default=forme_contact.TELEPHONE, choices=forme_contact.choices, verbose_name='Forme')
    etat = models.IntegerField(default=etat.OUVERTURE, choices=etat.choices, verbose_name='Etat')
    utilisateur = models.ForeignKey(User, verbose_name='Contact', on_delete=models.CASCADE)
    probleme = models.ForeignKey(probleme, verbose_name='Symptômes', on_delete=models.CASCADE)
    cause = models.ForeignKey(cause, verbose_name='Causes', on_delete=models.CASCADE, null=True, blank=True)
    detail = models.TextField(verbose_name="Détail", null=True, blank=True)
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


    def __str__(self):
        return str(self.evenement) + ' ' + str(etat(self.etat).name) + ' ' + str(self.probleme)

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




