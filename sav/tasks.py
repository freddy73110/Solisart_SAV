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

from Solisart_SAV.celery import app
from heraklesinfo.models import *
from .scrapping import send_channel_message

TextField.register_lookup(Length, "length")
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import *
import time
import io, os
from PIL import Image

from django.contrib import messages

import pandas as pd
import numpy as np

from django.utils import timezone


def save_result_celery(args, kwargs, status, result):

    # for current func name, specify 0 or no argument.
    # for name of caller of current func, specify 1.
    # for name of caller of caller of current func, specify 2. etc.
    currentFuncName = lambda n=1: sys._getframe(n + 1).f_code.co_name
    from django_celery_results.models import TaskResult
    import uuid

    from django.conf import settings

    task = TaskResult.objects.create(
        task_id=uuid.uuid4(),
        task_name=currentFuncName(),
        task_args=args,
        task_kwargs=kwargs,
        status=status,
        content_type="application/json",
        content_encoding="utf-8",
        result=result,
        traceback="-",
        meta={"DEGUB": str(settings.DEBUG)},
    )


@app.task
def wrapperscapping(func, kwargs):
    from .scrapping import scrappingMySolisart

    print(kwargs)
    return getattr(scrappingMySolisart(), func)(kwargs)


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
        commerciaux = profil_user.objects.filter(
            departement__isnull=False, mailOcommercial=True
        )
        result = {}
        for commercial in commerciaux:
            try:
                # list des tickets par affectation commerciale
                ticketscree = (
                    ticket.objects.filter(
                        evenement__date__gte=timezone.now() - timedelta(days=10),
                        evenement__installation__attribut_valeur__attribut_def__description="Code postal",
                    )
                    .annotate(
                        instal_id=Subquery(
                            installation.objects.filter(
                                evenement__ticket__id=OuterRef("id")
                            ).values("id")[:1]
                        ),
                        num_departement1=Subquery(
                            attribut_valeur.objects.filter(
                                installation__pk=OuterRef("instal_id"),
                                attribut_def__description="Code postal",
                            ).values("valeur")[:1]
                        ),
                        num_departement2=Substr("num_departement1", 1, 2),
                        num_departement=Case(
                            When(num_departement1__length=4, then=Value(str(100))),
                            When(num_departement1__length=5, then="num_departement2"),
                            output_field=CharField(),
                        ),
                    )
                    .filter(num_departement__in=list(commercial.departement))
                )
                ticketsencours = (
                    ticket.objects.filter(
                        etat__in=[0, 1, 2],
                        evenement__installation__attribut_valeur__attribut_def__description="Code postal",
                    )
                    .annotate(
                        instal_id=Subquery(
                            installation.objects.filter(
                                evenement__ticket__id=OuterRef("id")
                            ).values("id")[:1]
                        ),
                        num_departement1=Subquery(
                            attribut_valeur.objects.filter(
                                installation__pk=OuterRef("instal_id"),
                                attribut_def__description="Code postal",
                            ).values("valeur")[:1]
                        ),
                        num_departement2=Substr("num_departement1", 1, 2),
                        num_departement=Case(
                            When(num_departement1__length=4, then=Value(str(100))),
                            When(num_departement1__length=5, then="num_departement2"),
                            output_field=CharField(),
                        ),
                    )
                    .filter(num_departement__in=list(commercial.departement))
                )
                html_content = render_to_string(
                    "email/mailPourCommerciaux.html",
                    {
                        "ticketscree": ticketscree,
                        "ticketsencours": ticketsencours,
                        "commercial": commercial,
                    },
                )
                if ticketscree or ticketsencours:
                    msg = EmailMultiAlternatives(
                        "Solisart SAV: Rapport des derniers tickets sur votre périmètre",
                        "",
                        "sav@solisart.fr",
                        [commercial.user.email],
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                result[str(commercial)] = {
                    "ticketscree": len(ticketscree),
                    "ticketsencours": len(ticketsencours),
                }
            except Exception as ex:

                exc_type, exc_obj, exc_tb = sys.exc_info()

                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

                print(exc_type, fname, exc_tb.tb_lineno)

                print(ex)
                result[str(commercial)] = {"ERROR": "Error" + str(ex)}

        save_result_celery("args", {}, "SUCCESS", result)
        return json.dumps(result)

    except Exception as ex:

        exc_type, exc_obj, exc_tb = sys.exc_info()

        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

        print(exc_type, fname, exc_tb.tb_lineno)

        print(ex)

        save_result_celery("args", {}, "ERROR", "Error" + str(ex))

        return "Error" + str(ex)


@shared_task
def Recuperation_schema_my_solisart():
    """
    Non tester
    Logiquement des drivers pour firefox sont installé
    :return:
    """
    from bs4 import BeautifulSoup
    import requests

    username = "freddy.dubouchet@solisart.fr"
    password = "uM(ij9ojEV"
    link = "https://my.solisart.fr/"

    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import sys

    # non tester
    if "runserver" in sys.argv:
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Firefox(
            executable_path=r"C:\Users\freddy\Downloads\geckodriver-v0.32.0-win32\geckodriver.exe"
        )
    driver.get(link)
    driver.find_element(By.ID, "id").send_keys(username)
    driver.find_element(By.ID, "pass").send_keys(password)
    driver.find_element(By.ID, "connexion").click()
    for instal in installation.objects.all():
        idsa = instal.idsa
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

        driver.get(
            "https://my.solisart.fr/admin/index.php?page=installation&id=" + idsa
        )
        time.sleep(8)
        tt = driver.find_element(By.XPATH, '//label[@for="input-pages-visualisation"]')
        tt.click()
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(8)
        src = soup.find("img", {"id": "schema-image"})["src"]
        driver.get("https://my.solisart.fr/admin/" + src)
        # Enregistrement du fichier à la racine
        driver.save_screenshot("schema.png")

        # Creation Fichiers
        file = Fichiers.objects.create(titre=idsa + ".png")
        # driver.save_screenshot(idsa+'.png')
        namefile = idsa + ".png"

        image = Image.open("schema.png")
        # image = Image.open(namefile) #fonctionne avec un fichier exitant

        photo = io.BytesIO()
        image.save(photo, "png")
        # Sauvegarde de image
        f = file.fichier.save(namefile, ContentFile(photo.getvalue()))
        instal.schema_installation = f
        instal.save()
        # supprimer le fichier à la racine
        os.remove("schema.png")
        # Fermer le navigateur firefox

    driver.close()


@shared_task
def trouvercoordonneeGPSinstallateur(*args, **kwargs):
    """
    Cherche toutes les installateur qui n'ont pas de coordonnées GPS pour lui en affecter une
    1. via l'adresse de l'install
    2.via la commune de l'install
    4. sinon pas d'affectation
    :param *args:
    :param **kwargs:
    :return:
    """
    # liste de toutes les installation sans coordonnées GPS
    installateur_whitout_GPS = profil_user.objects.filter(
        Client_herakles__isnull=False, latitude__isnull=True
    )
    import requests

    counter = 0
    for installateur in installateur_whitout_GPS:
        try:
            adresse = C100Clients.objects.db_manager("herakles").get(
                t100_1_code_client__exact=installateur.Client_herakles
            )
            url = "https://nominatim.openstreetmap.org/?q=France"
            for at in [
                adresse.t100_4_adresse_1,
                adresse.t100_6_cp,
                adresse.t100_7_ville_pays,
            ]:
                url += "+" + str(at).replace(" ", "%")
            url += "&format=json"

            resp = requests.get(url).json()

            if not resp or not "lon" in resp[0]:
                url = "https://nominatim.openstreetmap.org/?q=France"
                for at in [adresse.t100_6_cp, adresse.t100_7_ville_pays]:
                    url += "+" + str(at).replace(" ", "%")
                url += "&format=json"
                resp = requests.get(url).json()
                if resp and "lon" in resp[0]:
                    GPS = resp[0]["lat"] + "," + resp[0]["lon"]
                else:
                    GPS = None
                    pass
            else:
                GPS = resp[0]["lat"] + "," + resp[0]["lon"]

            if GPS == "46.603354,1.8883335":
                GPS = None

            if GPS:
                installateur.latitude = GPS.split(",")[0]
                installateur.longitude = GPS.split(",")[1]
                installateur.save()
                counter += 1

        except Exception as ex:

            print(installateur)

            exc_type, exc_obj, exc_tb = sys.exc_info()

            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(exc_type, fname, exc_tb.tb_lineno)

            print(ex)
    save_result_celery(
        args,
        kwargs,
        "SUCCESS",
        str(counter)
        + "installateur localisé sur "
        + str(installateur_whitout_GPS.count()),
    )

    return {
        "bilan",
        str(counter)
        + "installateur localisé sur "
        + str(installateur_whitout_GPS.count()),
    }


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
    # liste de toutes les installation sans coordonnées GPS
    install_whitout_GPS = installation.objects.exclude(
        id__in=attribut_valeur.objects.filter(
            attribut_def__description="Coordonnées GPS DD"
        ).values_list("installation__id", flat=True)
    )
    import requests

    counter = 0
    for install in install_whitout_GPS:
        try:
            atts = attribut_valeur.objects.filter(installation=install)
            url = "https://nominatim.openstreetmap.org/?q=France"
            for at in atts:
                if at.attribut_def.description in ["Voie 1", "Code postal", "Commune"]:
                    url += "+" + at.valeur.replace(" ", "%")
            url += "&format=json"

            resp = requests.get(url).json()
            if not resp or not "lon" in resp[0]:
                url = "https://nominatim.openstreetmap.org/?q=France"
                for at in atts:
                    if at.attribut_def.description in ["Code postal", "Commune"]:
                        url += "+" + at.valeur.replace(" ", "%")
                url += "&format=json"
                resp = requests.get(url).json()
                if resp and "lon" in resp[0]:
                    GPS = resp[0]["lat"] + "," + resp[0]["lon"]
                else:
                    GPS = None
                    pass
            else:
                GPS = resp[0]["lat"] + "," + resp[0]["lon"]

            if GPS == "46.603354,1.8883335" and install.proprio():
                url = "https://nominatim.openstreetmap.org/?q=France"
                if install.proprio().profil_user.voie1 != "nan":
                    url += "+" + str(install.proprio().profil_user.voie1)
                if install.proprio().profil_user.voie1 != "nan":
                    url += "+" + str(install.proprio().profil_user.codepostal)
                if install.proprio().profil_user.voie1 != "nan":
                    url += "+" + str(install.proprio().profil_user.commune)
                url += "&format=json"
                resp = requests.get(url).json()
                if resp and "lon" in resp[0]:
                    GPS = resp[0]["lat"] + "," + resp[0]["lon"]
                else:
                    GPS = None
                    pass
            # Si localiser en France ne pas données de coordonnées GPS
            if GPS == "46.603354,1.8883335":
                GPS = None
            if GPS:
                attribut_valeur.objects.create(
                    installation=install,
                    attribut_def=attribut_def.objects.get(
                        description="Coordonnées GPS DD"
                    ),
                    valeur=GPS,
                )
                counter += 1

        except Exception as ex:

            print(install, resp, url)

            exc_type, exc_obj, exc_tb = sys.exc_info()

            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]

            print(exc_type, fname, exc_tb.tb_lineno)

            print(ex)
    save_result_celery(
        args,
        kwargs,
        "SUCCESS",
        counter + "instal localisé sur " + install_whitout_GPS.count(),
    )

    return {"bilan", counter + "instal localisé sur " + install_whitout_GPS.count()}


@shared_task
def actualise_date_livraison_CL():
    CLs = CL_herakles.objects.filter(
        date_livraison_prevu__gte=timezone.now() - timedelta(days=21)
    )
    result = []
    for CL in CLs:
        # before = date avavnt modif
        before = CL.date_livraison_prevu
        CL.date_livraison_prevu = (
            C601ChantierEnTte.objects.db_manager("herakles")
            .filter(t601_1_code_chantier=CL)
            .values_list("delai", flat=True)[0]
        )
        CL.save()
        from zoneinfo import ZoneInfo

        utc = ZoneInfo("UTC")
        if before != CL.date_livraison_prevu.date():
            result.append(
                {
                    "Name": CL.CL,
                    "newdate": CL.date_livraison_prevu.date().strftime("%d/%m/%Y"),
                    "olddate": before.strftime("%d/%m/%Y"),
                }
            )
        # Recherche si un BL a été créé pour cette CL
        if (
            C701Ouvraof.objects.db_manager("herakles")
            .filter(codechantier=CL)
            .exclude(codeof__icontains=CL)
        ):
            try:                
                CL.BL = BL_herakles.objects.get(
                BL=C701Ouvraof.objects.db_manager("herakles")
                .filter(codechantier=CL)
                .exclude(codeof__icontains=CL)
                .values_list("codeof", flat=True)[0]
                )
            except:
                print(C701Ouvraof.objects.db_manager("herakles")
                .filter(codechantier=CL)
                .exclude(codeof__icontains=CL)
                .values_list("codeof", flat=True)[0])
                print("error for ", CL)
                pass
        CL.save()

        trans = (
            C7001Phases.objects.db_manager("herakles")
            .filter(codechantier=CL, codetransporteur__isnull=False)
            .values_list("codetransporteur", flat=True)
        )
        if trans:
            if not transporteur.objects.filter(nom=trans[0]).exists():
                transp = transporteur.objects.create(nom=trans[0])
            else:
                transp = transporteur.objects.get(nom=trans[0])
            CL.transporteur = transp
            CL.save()

    send_channel_message(
        "production",
        {
            "message": "Les dates de livraison client viennent d'être mise à jour",
            "result": result,
            "datereceptionclient": True,
        },
    )

    save_result_celery("args", {}, "SUCCESS", result)


@shared_task
def actualise_client_herakles():

    result = {"Client": []}
    clients = C100Clients.objects.db_manager("herakles").all()
    for client in clients:
        try:
            client_herakles.objects.get(Code_Client=client.t100_1_code_client)
            created = False
        except:
            c = client_herakles.objects.create(
                Code_Client=client.t100_1_code_client, Nom=client.t100_3_nom
            )
            created = True
        if created:
            result["Client"].append(c.Code_Client)
    save_result_celery("args", {}, "SUCCESS", result)


@shared_task
def actualise_herakles():
    result = {"BLcree": [], "Deviscree": []}
    # actualisation les devis

    devis = (
        C101DevisEnTte.objects.db_manager("herakles")
        .filter(t101_1_code_devis__icontains="D" + str(timezone.now().year)[2:4])
        .order_by("-t101_1_code_devis")[:30:-1]
    )

    for d in devis:
        p, created = devis_herakles.objects.get_or_create(
            devis=str(d.t101_1_code_devis).split("/")[0]
        )
        if created:
            result["Deviscree"].append(d)

    # actualisation des BL
    BLs = (
        C7001Phases.objects.db_manager("herakles")
        .filter(codephase__icontains="BL" + str(timezone.now().year)[2:4])
        .order_by("-codephase")
        .values_list("codephase", flat=True)[:30:-1]
    )
    for BL in BLs:
        p, created = BL_herakles.objects.get_or_create(BL=BL)
        if created:
            result["BLcree"].append(BL)

    save_result_celery("args", {}, "SUCCESS", result)


@shared_task
def actualisePrixMySolisart(*args, **kwargs):

    from django.db.models import F
    from django.db.models import FloatField
    from django.db.models.functions import Cast

    articles = (
        B50Composants.objects.db_manager("herakles")
        .all()
        .annotate(
            ref=F("t50_2_code_comp"),
            prix=Cast(
                "t50_35_prix_de_vente_ouvrage_catalogue", output_field=(FloatField())
            ),
            label=F("t50_37_titre_du_composant"),
            tarif = F("t50_21_2_identificateur_hiérarchique_2")
        )
        .values("ref", "prix", "label", "tarif")
    )

    import requests

    # URL de l'endpoint POST
    url_dev = "https://www.solisart.fr/schematics/api/updateTarif.php"

    # En-têtes de la requête
    headers = {"Content-Type": "application/json; charset=latin-1"}

    # Envoi de la requête POST avec les données JSON
    response = requests.post(url_dev, json=list(articles), headers=headers)

    # Vérification du statut de la réponse
    if response.status_code == 200:
        print("Requête POST réussie.", response.status_code, response.text)
    else:
        print(
            "Erreur lors de la requête POST. Code de statut:",
            response.status_code,
            response.text,
        )

    save_result_celery("args", list(articles), "SUCCESS", response.text)

    return HttpResponse(
        "Requête code: "
        + str(response.status_code)
        + " <br> "
        + str(response.text).replace("\n", "<br>")
    )


@shared_task
def cleanTaskResult(*args, **kwargs):
    from django_celery_results.models import TaskResult
    from django.db.models import Max

    tasks = (
        TaskResult.objects.all()
        .order_by("task_name")
        .values("task_name")
        .annotate(Max("id"))
        .values_list("id__max", flat=True)
    )
    TaskResult.objects.exclude(id__in=tasks).delete()
    save_result_celery(
        "args",
        {},
        "SUCCESS",
        [
            str(f)
            for f in TaskResult.objects.all()
            .order_by("task_name")
            .values("task_name")
            .annotate(Max("id"))
        ],
    )


@shared_task
def ActualiseUtilisateur(*args, **kwargs):
    df_as_dict = kwargs.get("df_as_dict")
    df = pd.DataFrame.from_dict(df_as_dict)
    df.columns = [
        "id",
        "pass",
        "nom",
        "prenom",
        "email",
        "telephone1",
        "telephone2",
        "voie1",
        "voie2",
        "voie3",
        "codepostal",
        "commune",
    ]
    df = df.reset_index()  # make sure indexes pair with number of rows
    total_created = 0
    lendf = str(len(df))
    send_channel_message(
        "updateDB",
        {
            "message": "Démarrage de la mise en base de donnée.<br>utilisateur: 0/"
            + lendf,
            "index": 0,
            "total": lendf,
            "nature": "utilisateurs",
        },
    )
    for index, row in df.iterrows():
        try:
            user, created = User.objects.get_or_create(username=row["id"])
            user.first_name = (row["prenom"],)
            user.last_name = (row["nom"],)
            user.email = row["email"]
            # Comprend pas cette ligne mais çà marche
            user.first_name = user.first_name[0]
            user.last_name = user.last_name[0]
            user.save()
            profil = profil_user.objects.get(user=user)
            profil.idsa = row["id"]
            profil.PW = row["pass"]
            profil.telephone1 = (
                row["telephone1"]
                if str(row["telephone1"]).replace(".", "").replace(" ", "")
                != profil.telephone1
                else profil.telephone1
            )
            profil.telephone2 = (
                row["telephone2"]
                if str(row["telephone2"]).replace(".", "").replace(" ", "")
                != profil.telephone2
                else profil.telephone2
            )
            profil.voie1 = row["voie1"]
            profil.voie2 = row["voie2"]
            profil.voie3 = row["voie3"]
            profil.codepostal = row["codepostal"]
            profil.commune = row["commune"]
            profil.save()
            if created:
                total_created += 1

        except Exception as e:
            print(row)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            pass

        if index % 100 == 0:
            send_channel_message(
                "updateDB",
                {
                    "message": "En cours d'éxécution:<br>utilisateurs: "
                    + str(index)
                    + "/"
                    + lendf,
                    "index": index,
                    "total": lendf,
                    "nature": "utilisateurs",
                },
            )

    send_channel_message(
        "updateDB",
        {
            "message": "Importation finie:<br>utilisateurs: " + lendf + "/" + lendf,
        },
    )
    save_result_celery(
        "args", {}, "SUCCESS", str(total_created) + " nouveaux utilisateurs de créer"
    )


@shared_task
def ActualiseInstallation(*args, **kwargs):
    df_as_dict = kwargs.get("df_as_dict")
    df = pd.DataFrame.from_dict(df_as_dict)
    lendf = str(len(df))
    df.columns = [
        "id",
        "type_communication",
        "version_carte_firmware",
        "version_carte_interface",
        "version_serveur_appli",
        "heure_contact",
        "heure_test",
        "adresse_ip_wan",
        "port_tcp_wan",
        "	propager_droits",
    ]
    df = df.reset_index()  # make sure indexes pair with number of rows
    total_created = 0
    send_channel_message(
        "updateDB",
        {
            "message": "Démarrage de la mise en base de donnée.<br>installation: 0/"
            + lendf,
        },
    )
    for index, row in df.iterrows():
        try:
            inst, created = installation.objects.get_or_create(idsa=row["id"])
            # tc= row['type_communication'] if row['type_communication'] != np.nan else None

            # inst.type_communication= tc,

            inst.version_carte_firmware = (
                (
                    row["version_carte_firmware"]
                    if "version_carte_firmware" in row
                    and row["version_carte_firmware"] != np.nan
                    else None
                ),
            )
            inst.version_carte_interface = (
                (
                    row["version_carte_interface"]
                    if "version_carte_interface" in row
                    and row["version_carte_interface"] != np.nan
                    else None
                ),
            )
            inst.version_serveur_appli = (
                (
                    row["version_serveur_appli"]
                    if "version_serveur_appli" in row
                    and row["version_serveur_appli"] != np.nan
                    else None
                ),
            )
            inst.adresse_ip_wan = (
                (
                    row["adresse_ip_wan"]
                    if "adresse_ip_wan" in row and row["adresse_ip_wan"] != np.nan
                    else None
                ),
            )
            inst.port_tcp_wan = (
                row["port_tcp_wan"]
                if "port_tcp_wan" in row and row["port_tcp_wan"] != np.nan
                else None
            )
            inst.save()

            if created:
                total_created += 1

        except Exception as e:
            print(row)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            pass
        if index % 100 == 0:
            send_channel_message(
                "updateDB",
                {
                    "message": "En cours d'éxécution:<br>installation: "
                    + str(index)
                    + "/"
                    + lendf,
                    "index": index,
                    "total": lendf,
                    "nature": "installations",
                },
            )
    send_channel_message(
        "updateDB",
        {
            "message": "Importation finie:<br>installations: " + lendf + "/" + lendf,
        },
    )

    save_result_celery(
        "args", {}, "SUCCESS", str(total_created) + " nouvelles installations"
    )


@shared_task
def ActualiseAcces(*args, **kwargs):
    df_as_dict = kwargs.get("df_as_dict")
    df = pd.DataFrame.from_dict(df_as_dict)
    lendf = str(len(df))
    df.columns = ["utilisateur", "profil", "installation"]
    df = df.reset_index()  # make sure indexes pair with number of rows
    total_created = 0
    send_channel_message(
        "updateDB",
        {
            "message": "Démarrage de la mise en base de donnée.<br>accès: 0/" + lendf,
        },
    )
    for index, row in df.iterrows():
        try:
            int, created = acces.objects.get_or_create(
                installation=installation.objects.get(idsa=row["installation"]),
                profil_type=profil_type.objects.get(idsa=row["profil"]),
                utilisateur=User.objects.get(profil_user__idsa=row["utilisateur"]),
            )
            if created:
                total_created += 1

        except Exception as e:
            print(row)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            pass
        if index % 500 == 0:
            send_channel_message(
                "updateDB",
                {
                    "message": "En cours d'éxécution:<br>accès: "
                    + str(index)
                    + "/"
                    + lendf,
                    "index": index,
                    "total": lendf,
                    "nature": "accès",
                },
            )
    send_channel_message(
        "updateDB",
        {
            "message": "Importation finie:<br>accès: " + lendf + "/" + lendf,
        },
    )
    save_result_celery("args", {}, "SUCCESS", str(total_created) + " nouveaux acces")


@shared_task
def ActualiseHistorique(*args, **kwargs):
    df_as_dict = kwargs.get("df_as_dict")
    df = pd.DataFrame.from_dict(df_as_dict)
    lendf = str(len(df))
    df.columns = ["installation", "heure", "donnee", "valeur"]
    df = df.reset_index()  # make sure indexes pair with number of rows
    total_created = 0
    send_channel_message(
        "updateDB",
        {
            "message": "Démarrage de la mise en base de donnée.<br>historique: 0/"
            + lendf,
        },
    )
    for index, row in df.iterrows():
        try:
            int, created = historique.objects.get_or_create(
                installation=installation.objects.get(idsa=row["installation"]),
                donnee=donnee.objects.get(idsa=row["donnee"]),
            )
            int.valeur = row["valeur"]
            int.save()
            if created:
                total_created += 1

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            pass
        if index % 100 == 0:
            send_channel_message(
                "updateDB",
                {
                    "message": "En cours d'éxécution:<br>historique: "
                    + str(index)
                    + "/"
                    + lendf,
                    "index": index,
                    "total": lendf,
                    "nature": "historiques",
                },
            )
    send_channel_message(
        "updateDB",
        {
            "message": "Importation finie:<br>historique: " + lendf + "/" + lendf,
        },
    )
    save_result_celery(
        "args", {}, "SUCCESS", str(total_created) + " nouveaux historiques"
    )


@shared_task
def ActualiseAttribut(*args, **kwargs):
    df_as_dict = kwargs.get("df_as_dict")
    df = pd.DataFrame.from_dict(df_as_dict)
    lendf = str(len(df))
    df.columns = ["installation", "attribut_def", "valeur"]
    df = df.reset_index()  # make sure indexes pair with number of rows
    total_created = 0
    send_channel_message(
        "updateDB",
        {
            "message": "Démarrage de la mise en base de donnée.<br>attribut_def: 0/"
            + lendf,
        },
    )
    for index, row in df.iterrows():
        try:
            int, created = attribut_valeur.objects.get_or_create(
                installation=installation.objects.get(idsa=row["installation"]),
                attribut_def=attribut_def.objects.get(idsa=row["attribut_def"]),
            )
            int.valeur = row["valeur"]
            int.save()
            if created:
                total_created += 1

        except Exception as e:

            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e)
            pass
        if index % 500 == 0:
            send_channel_message(
                "updateDB",
                {
                    "message": "En cours d'éxécution:<br>attribut_val: "
                    + str(index)
                    + "/"
                    + lendf,
                    "index": index,
                    "total": lendf,
                    "nature": "valeurs d'attribut",
                },
            )
    send_channel_message(
        "updateDB",
        {
            "message": "Importation finie:<br>attribut_val: " + lendf + "/" + lendf,
        },
    )
    save_result_celery(
        "args", {}, "SUCCESS", str(total_created) + " nouveaux historiques"
    )

@shared_task
def TestGTC(*args, **kwargs):
    from pyModbusTCP.client import ModbusClient
    import logging

    from pyModbusTCP.client import ModbusClient

    #documentation
    #https://pymodbustcp.readthedoc sudo pip3 install pyModbusTCP --upgrades.io/en/latest/package/class_ModbusClient.html

    # set debug level for pyModbusTCP.client to see frame exchanges
    logging.basicConfig()
    logging.getLogger('pyModbusTCP.client').setLevel(logging.DEBUG)
    host = "195.110.34.131" if not 'host' in kwargs else kwargs['host']
    port=502 if not 'port' in kwargs else kwargs['port']
    unit_id=1 if not 'unit_id' in kwargs else kwargs['unit_id']

    # TCP auto connect on first modbus request
    c = ModbusClient(host=host, port=port, unit_id=unit_id, auto_open=True, auto_close=False)
    now = datetime.datetime.now()
    

    file_path=os.path.join(os.path.dirname(__file__), "static", "TestTCP.csv")

    if not os.path.exists(file_path):
        with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
            import csv
            writer = csv.writer(csvfile, delimiter=';')  # Utiliser le point-virgule comme séparateur
            
            writer.writerow(['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'T10', 'T11', 'T12', 'T13', 'T14', 'T15', 'T16', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'APP', 'SOL', 'BTC', 'C7', 'C1', 'C2','C3', 'CHDR1', 'CHDR2', 'V3VSOL', 'V3VAPP', 'Tmesure', 'VolECS', 'EnECSSol', 'EnECSApp', 'EnECSTot', 'TmoyECS', 'TmoyECSfroid', 'ENChaufSol', 'ENChauffApp', 'ENChauffTot'])

    with open(file_path, 'a', newline='', encoding='utf-8') as csvfile:
        import csv
        writer = csv.writer(csvfile, delimiter=';')  # Utiliser le point-virgule comme séparateur
        writer.writerow([now.strftime("%d/%m/%y %H:%M:%S")] + c.read_holding_registers(0, 21) + c.read_input_registers(21, 21))

    csvfile.close()

    # c.read_coils(0)
    # adresses=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 16, 17, 18, 19]
    # for i in adresses:
    #     #Fonction 4
    #     regs = c.read_holding_registers(i, 1)
    #     if regs:
    #         print(i, regs)
    #     else:
    #         print(i, "read error")

    # for i in adresses:
    #     #fonction 3
    #     regs = c.read_input_registers(i, 1)
    #     if regs:
    #         print(i, regs)
    #     else:
    #         print(i, "read error")

    # for i in adresses:
    #     #fonction 1
    #     regs = c.read_coils(i, 1)
    #     if regs:
    #         print(i, regs)
    #     else:
    #         print(i, "read error")

    # for i in adresses:
    #     #fonction 2
    #     regs = c.read_discrete_inputs(i, 1)
    #     if regs:
    #         print(i, regs)
    #     else:
    #         print(i, "read error")

    c.close()
    save_result_celery(args, kwargs, "SUCCESS", "null")

@shared_task
def TestGTCdownload(*args, **kwargs):
    from django.core.mail import EmailMessage
    from email.mime.base import MIMEBase
    from email import encoders

    sendto = 'freddy.dubouchet@solisart.fr' if not "sendto" in kwargs else kwargs['sendto']

    email = EmailMessage(
        'Fichier csv pour test ModBus IP',
        'Voilà le fichier en question',
        'sav@solisart.fr',
        [sendto],
    )

    # Attacher une pièce jointe
    file_path=os.path.join(os.path.dirname(__file__), "static", "TestTCP.csv")
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= TestTCP.csv")
        email.attach(part)

    email.send()