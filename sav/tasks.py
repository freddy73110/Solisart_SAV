# -*- coding: utf-8 -*-
import datetime
import json
import sys

from asgiref.sync import async_to_sync
from celery import shared_task
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Subquery, OuterRef, When, Value, CharField, TextField, Case
from django.db.models.functions import Substr, Lower
from django.db.models.functions import Length

from heraklesinfo.models import *

TextField.register_lookup(Length, 'length')
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import profil_user, ticket, Fichiers, installation, attribut_valeur, attribut_def, BL_herakles,\
    devis_herakles,client_herakles
import time
import io, os
from PIL import Image

def save_result_celery(args, kwargs, status, result):

    # for current func name, specify 0 or no argument.
    # for name of caller of current func, specify 1.
    # for name of caller of caller of current func, specify 2. etc.
    currentFuncName = lambda n=1: sys._getframe(n + 1).f_code.co_name
    from django_celery_results.models import TaskResult
    import uuid

    from django.conf import settings

    task = TaskResult.objects.create(
                    task_id = uuid.uuid4(),
                    task_name = currentFuncName(),
                    task_args = args,
                    task_kwargs = kwargs,
                    status = status,
                    content_type ="application/json",
                    content_encoding = "utf-8",
                    result = result,
                    traceback ="-",
                    meta={"DEGUB": str(settings.DEBUG)}
                )

@shared_task
def add(x, y):
    time.sleep(10)
    print(x, y)
    return str(x + y) + "Hello World"

# @shared_task
# def refresh_mailbox():
    # print("in refresh mailbox")
    # from .views import inbox
    # mailbox = inbox.mailbox_search(fetch=None, days=10)
    # for e in mailbox:
    #     print({'date':e.date,
    #                               'from_':e.from_,
    #                               'subject':e.subject,
    #                               # 'html':e.html,
    #                               # 'text':e.text,
    #                               'uid':e.uid,
    #                               # 'attachment': inbox.fileattchment(e),
    #                                 })
    #     try:
    #         msg = emailbox.objects.get(uid=e.uid)
    #     except:
    #         msg = emailbox.objects.create(
    #             uid=e.uid,
    #             subject = e.subject,
    #             de = e.from_,
    #             to = e.to,
    #             cc = e.cc,
    #             date = e.date,
    #             html = e.html,
    #             text = e.text
    #         )
    #         #envoi notification de mail entrant
    #     html_message = render_to_string(
    #                'widgets/toast_message.html',
    #                {
    #                    'msg':msg,
    #                    'now':datetime.datetime.now()
    #                })
    #     from channels.layers import get_channel_layer
    #     layer = get_channel_layer()
    #     async_to_sync(layer.group_send)('all',{'type':'chatroom_message','message':html_message, 'username':'moi'}
    #                                         )
    # msg = EmailMultiAlternatives("rapport des mails", "C'est fait!", "sav@solisart.fr", ["freddy.dubouchet@gmail.com"])
    # msg.send()

    # mailbox = inbox.mailbox_search(days=30)
    # i = 0
    # print("pourquoi?", mailbox)
    # for msg in mailbox:
    #     i+=1
    #     print('message ', i, ' :' ,msg.subject, msg.from_)
    # print("nb d'mail: ", i)

@shared_task
def rapport_ticket():
    try:
        commerciaux = profil_user.objects.filter(departement__isnull=False, mailOcommercial=True)
        result = {}
        for commercial in commerciaux:
            #list des tickets par affectation commerciale
            ticketscree = ticket.objects.filter(
                evenement__date__gte=datetime.date.today() - datetime.timedelta(days=10),
                evenement__installation__attribut_valeur__attribut_def__description="Code postal",
            ).annotate(
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
            ).filter(num_departement__in=list(commercial.departement))
            ticketsencours = ticket.objects.filter(
                etat__in =[0, 1, 2],
                evenement__installation__attribut_valeur__attribut_def__description="Code postal",
            ).annotate(
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
            ).filter(num_departement__in=list(commercial.departement))
            html_content = render_to_string('email/mailPourCommerciaux.html', {
                'ticketscree': ticketscree,
                'ticketsencours': ticketsencours,
                'commercial': commercial
            })
            if ticketscree or ticketsencours:
                msg = EmailMultiAlternatives("Solisart SAV: Rapport des derniers tickets sur votre périmètre", '', "sav@solisart.fr", [commercial.user.email])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            result[str(commercial)]={'ticketscree': len(ticketscree), 'ticketsencours':len(ticketsencours)}

        save_result_celery('args', {}, "SUCCESS", result)
        return json.dumps(result)


    except Exception as ex:

        exc_type, exc_obj, exc_tb = sys.exc_info()

        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        print(exc_type, fname, exc_tb.tb_lineno)

        print(ex)

        save_result_celery('args', {}, "ERROR", 'Error' + str(ex))

        return 'Error' + str(ex)

@shared_task
def Recuperation_schema_my_solisart():
    '''
    Non tester
    Logiquement des drivers pour firefox sont installé
    :return:
    '''
    from bs4 import BeautifulSoup
    import requests

    username = 'freddy.dubouchet@solisart.fr'
    password = 'uM(ij9ojEV'
    link = 'https://my.solisart.fr/'

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import sys
    #non tester
    if 'runserver' in sys.argv:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Firefox(
            executable_path=r"C:\Users\freddy\Downloads\geckodriver-v0.32.0-win32\geckodriver.exe")
    driver.get(link)
    driver.find_element(By.ID, 'id').send_keys(username)
    driver.find_element(By.ID, 'pass').send_keys(password)
    driver.find_element(By.ID, 'connexion').click()
    for instal in installation.objects.all():
        idsa=instal.idsa
        time.sleep(6)
        # soup = BeautifulSoup(driver.page_source,'html.parser')
        # tables = soup.find('table', {'class':'liste'})
        # all_td = tables.find_all("tr")
        # passed=0
        # for row in all_td:
        #     table_row=[r for r in row.find_all('td')]
        #     try:
        #         print(table_row[0].find_all("a")[1].text) #.find('span').text, table_row[1].text, table_row[2], table_row[3], table_row[4], table_row[5])
        #     except:
        #         passed+=1
        #         pass
        # print(passed)
        # print(len(all_td))

        driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + idsa)
        time.sleep(8)
        tt = driver.find_element(By.XPATH, '//label[@for="input-pages-visualisation"]')
        tt.click()
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        time.sleep(8)
        src = soup.find('img', {'id': 'schema-image'})['src']
        driver.get(
            'https://my.solisart.fr/admin/' + src)
        # Enregistrement du fichier à la racine
        driver.save_screenshot("schema.png")

        # Creation Fichiers
        file = Fichiers.objects.create(
            titre=idsa + '.png'
        )
        # driver.save_screenshot(idsa+'.png')
        namefile = idsa + '.png'

        image = Image.open("schema.png")
        # image = Image.open(namefile) #fonctionne avec un fichier exitant

        photo = io.BytesIO()
        image.save(photo, "png")
        # Sauvegarde de image
        f = file.fichier.save(namefile, ContentFile(photo.getvalue()))
        instal.schema_installation=f
        instal.save()
        # supprimer le fichier à la racine
        os.remove("schema.png")
        # Fermer le navigateur firefox

    driver.close()

@shared_task
def trouvercoordonneeGPS(*args, **kwargs):
    """
    Cherche toutes les inatallation qui n'ont pas de coordonnées GPS pour lui en affecter une
    1. via l'adresse de l'install
    2.via la commune de l'install
    3. via l'adresse du priprio de l'install
    4. sinon pas d'affectation
    :param *args:
    :param **kwargs:
    :return:
    """
    #liste de toutes les installation sans coordonnées GPS
    install_whitout_GPS = installation.objects.exclude(
        id__in=attribut_valeur.objects.filter(attribut_def__description='Coordonnées GPS DD').values_list(
            'installation__id', flat=True)
    )
    import requests
    counter = 0
    for install in install_whitout_GPS:
        try:
            atts = attribut_valeur.objects.filter(installation = install)
            url = 'https://nominatim.openstreetmap.org/?q=France'
            for at in atts:
                if at.attribut_def.description in ["Voie 1", "Code postal", "Commune"] :
                    url += '+' + at.valeur.replace(' ','%')
            url += '&format=json'

            resp = requests.get(url).json()
            if not resp or not 'lon' in resp[0]:
                url = 'https://nominatim.openstreetmap.org/?q=France'
                for at in atts:
                    if at.attribut_def.description in ["Code postal", "Commune"]:
                        url += '+' + at.valeur.replace(' ', '%')
                url += '&format=json'
                resp = requests.get(url).json()
                if resp and 'lon' in resp[0]:
                    GPS = resp[0]['lat'] + ',' + resp[0]['lon']
                else:
                    GPS = None
                    pass
            else:
                GPS= resp[0]['lat'] + ',' + resp[0]['lon']

            if GPS == '46.603354,1.8883335' and install.proprio():
                url = 'https://nominatim.openstreetmap.org/?q=France'
                if install.proprio().profil_user.voie1 != 'nan':
                    url+= '+'+str(install.proprio().profil_user.voie1)
                if install.proprio().profil_user.voie1 != 'nan':
                    url+= '+'+str(install.proprio().profil_user.codepostal)
                if install.proprio().profil_user.voie1 != 'nan':
                    url+= '+'+str(install.proprio().profil_user.commune)
                url += '&format=json'
                resp = requests.get(url).json()
                if resp and 'lon' in resp[0]:
                    GPS = resp[0]['lat'] + ',' + resp[0]['lon']
                else:
                    GPS = None
                    pass
            #Si localiser en France ne pas données de coordonnées GPS
            if GPS == '46.603354,1.8883335':
                GPS = None
            if GPS:
                attribut_valeur.objects.create(
                    installation = install,
                    attribut_def = attribut_def.objects.get(description = 'Coordonnées GPS DD'),
                    valeur = GPS
                )
                counter += 1

        except Exception as ex:

            print(install, resp, url)

            exc_type, exc_obj, exc_tb = sys.exc_info()

            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(exc_type, fname, exc_tb.tb_lineno)

            print(ex)
    save_result_celery(args, kwargs, "SUCCESS", counter+ 'instal localisé sur '+ install_whitout_GPS.count())

    return {'bilan', counter+ 'instal localisé sur '+ install_whitout_GPS.count()}

@shared_task
def actualise_client_herakles():
    result = {'Client': []}
    clients=C100Clients.objects.db_manager('herakles').all()
    for client in clients:
        c, created = client_herakles.objects.get_or_create(
            Code_Client=client.t100_1_code_client,
            Nom=client.t100_3_nom
        )
        if created:
            result['Client'].append(c.Code_Client)
    save_result_celery('args', {}, "SUCCESS", result)


@shared_task
def actualise_herakles():
    result = {'BLcree': [], 'Deviscree': []}
    #actualisation les devis
    devis = C101DevisEnTte.objects.db_manager('herakles').\
        filter(t101_1_code_devis__icontains='D' + str(datetime.date.today().year)[2:4]).\
        order_by('-t101_1_code_devis')[:30:-1]

    for d in devis:
        p, created = devis_herakles.objects.get_or_create(
                             devis=str(d.t101_1_code_devis).split('/')[0]
                         )
        if created:
            result['Deviscree'].append(d)

    #actualisation des BL
    BLs = C7001Phases.objects.db_manager('herakles').\
        filter(codephase__icontains='BL' + str(datetime.date.today().year)[2:4]).\
        order_by('-codephase').\
        values_list('codephase', flat=True)[:30:-1]
    for BL in BLs:
        p, created = BL_herakles.objects.get_or_create(
            BL=BL
        )
        if created:
            result['BLcree'].append(BL)

    save_result_celery('args', {}, "SUCCESS", result)

@shared_task
def actualisePrixMySolisart(*args, **kwargs):

    from django.db.models import F
    from django.db.models import FloatField
    from django.db.models.functions import Cast
    articles = B50Composants.objects.db_manager('herakles').all().annotate(
        ref = F("t50_2_code_comp"),
        prix = Cast("t50_35_prix_de_vente_ouvrage_catalogue", output_field=(FloatField())),
        label=F("t50_37_titre_du_composant")
    ).values("ref", "prix", "label")

    import requests

    # URL de l'endpoint POST
    url_dev = 'https://www.solisart.fr/schematics/api/updateTarif.php'


    # En-têtes de la requête
    headers = {
        'Content-Type': 'application/json'
    }

    # Envoi de la requête POST avec les données JSON
    response = requests.post(url_dev, json=list(articles), headers=headers)

    # Vérification du statut de la réponse
    if response.status_code == 200:
        print('Requête POST réussie.', response.status_code, response.text)
    else:
        print('Erreur lors de la requête POST. Code de statut:', response.status_code, response.text)

    save_result_celery('args', {}, "SUCCESS", response.text)

    return HttpResponse('Requête code: ' + str(response.status_code)+ " <br> " +  str(response.text).replace('\n', '<br>'))










