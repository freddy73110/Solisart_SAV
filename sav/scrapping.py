import glob
import json
import time

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import sys, os

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, expected_conditions

from .models import CL_herakles, installation

from django.utils import timezone


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location

    else:
        return os.path.join(os.path.abspath(os.sep), 'root', 'snap', 'firefox', '2952')

def send_channel_message(group_name, message):
    # Sous Windows
    if os.name =="nt":
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    message['type']='channel_message'

    if not 'processing' in message:
        message['processing']=True
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        message
    )


class scrappingMySolisart():
    username = 'freddy.dubouchet@solisart.fr'
    password = 'G2poilOQ'
    link = 'https://my.solisart.fr/'
    json_installation = False
    connecting=False

    def __init__(self):
        try:
            send_channel_message('cartcreating', {
                'message':'Lancement du scrapping',
                'processing': True
            })
            if not os.name =='nt':
                import subprocess
                if subprocess.call("killall -9 firefox", shell=True) > 0:
                    send_channel_message('cartcreating', {
                        'message': "Arrêt de Firefox"
                    })
                else:
                    send_channel_message('cartcreating', {
                        'message': 'Arrêt du firefox'
                    })

                from selenium import webdriver
                from selenium.webdriver import FirefoxOptions
                opts = FirefoxOptions()
                opts.add_argument("--headless")
                self.driver = webdriver.Firefox(options=opts)
            else:
                from selenium import webdriver
                from selenium.webdriver.firefox.service import Service
                service = Service(
                    executable_path=r"C:\Users\freddy\Downloads\geckodriver-v0.32.0-win32\geckodriver.exe"
                )
                self.driver = webdriver.Firefox(
                    service=service
                )
            # from selenium import webdriver
            # from selenium.webdriver.firefox.service import Service as FirefoxService
            # from webdriver_manager.firefox import GeckoDriverManager
            # from selenium.webdriver import FirefoxOptions
            # opts = FirefoxOptions()
            # opts.add_argument("--headless")
            # self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=opts)
            self.connecting=True
            self.driver.get(self.link)
            self.driver.find_element(By.ID, 'id').send_keys(self.username)
            self.driver.find_element(By.ID, 'pass').send_keys(self.password)
            self.driver.find_element(By.ID, 'connexion').click()
            send_channel_message('cartcreating', {
                'message':'Connexion au serveur my.solisart.fr'
            })
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Erreur: " + str(exc_type) + str(
                    fname) + str(exc_tb.tb_lineno) + str(ex)})


    def waitelement(self, by, element, func, action, time_max=None):
        if not time_max:
            time_max=20
        try:
            from selenium.common.exceptions import NoSuchElementException
            from selenium.common.exceptions import StaleElementReferenceException
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            wait = WebDriverWait(self.driver, time_max, ignored_exceptions=ignored_exceptions)
            element = wait.until(getattr(EC, func)((by, element)))
            if action == 'click':
                element.click()
            else:
                return element
        except TimeoutException:
            print("L'élément n'est pas apparu dans les "+time_max+" secondes.")
            self.close()


    def close(self):
        self.driver.close()
        send_channel_message('cartcreating', {
            'message':'Déconnexion au serveur my.solisart.fr',
            'processing':False
        })
        self.connecting = False

    def list_installation(self):
        """

        :return: la listes de toutes les installations sur my.solisart.fr au moment de la commande
        """

        self.driver.get('https://my.solisart.fr/admin/index.php?page=installations')
        send_channel_message('cartcreating', {
            'message': 'Connecté à la page des installations'
        })
        time.sleep(5)
        install = self.waitelement(By.XPATH, '//*[@class="liste_colonne_paire"]/a[2]', 'presence_of_all_elements_located', None, time_max=120)
        all_installs = []
        for i in install:
            all_installs.append(i.get_attribute("innerHTML"))
        return all_installs
    def save_csv_configuration(self, path_csv=None):
        """
        Depuis la page d'une installation, enregister le csv et sauvegarder les données
        :param csv: path depuis le fichier csv de configuration
        :return:
        """
        try:
            import csv
            file = open(path_csv)
            csv_file = csv.reader(file, delimiter=";")
            lines = list(csv_file)
            installation = lines[3][2]
            file.close()
            time.sleep(2)
            self.waitelement(By.XPATH, '//label[@for="input-pages-maj"]', 'presence_of_element_located', 'click')
            time.sleep(2)
            self.waitelement(By.XPATH, '//a[@href="#onglet-config"]', 'presence_of_element_located', 'click')
            time.sleep(2)
            self.driver.find_element(By.ID, "upload-input-3").send_keys(path_csv)
            time.sleep(2)
            self.driver.find_element(By.ID, "bouton-telecharger").click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="liste-configs"]/table/tbody/tr[2]/td[4]/a[1]').click()
            self.waitelement(By.XPATH, '//button[@title="Close"]', 'presence_of_element_located', 'click')
            time.sleep(10)
            self.driver.find_element(By.XPATH, '//a[@href="#onglet-enregistrement"]').click()
            self.driver.find_element(By.ID, 'button-enregistrement-enregistrer').click()
            send_channel_message(
                'cartcreating',{'message':"<i class='fas fa-check' style='color: #018303;'></i> Les informations pour " + installation + " sont bien enregistrées."}
            )
            SC_TEST = True

            try:
                self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + installation)
                i = 0
                while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                        "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                    time.sleep(0.5)
                    print("wait again")
                    i += 1
                if i == 1200:
                    print("La carte " + installation + " ne s'est pas connecté en 10 min")
                    installed_connecting = False
                else:
                    print("La carte " + installation + " est connectée")
                    installed_connecting = True
            except:
                installed_connecting =False

            if SC_TEST and not installed_connecting:
                i = 0
                send_channel_message('cartcreating', {'message':"Recherche de l'installation " + installation + " dans la liste des installations"})
                l = self.list_installation()
                while i < 30 and not installation in l:
                    i += 1
                    l = self.list_installation()
                if i == 30:
                    send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Abandon de de recherche d'installation " + installation})
                    self.close()
                else:
                    send_channel_message('cartcreating', {'message':'<i class="fas fa-check" style="color: #018303;"></i> Installation ' + installation + " dans la liste des installations"})
                    instal = installation
                    from .models import installation
                    installation.objects.create(idsa=instal)
                    send_channel_message('cartcreating', {'message':"Installation " + instal +" enregistrée dans le solistools"})
                    send_channel_message('cartcreating', {'message':"Préparation de l'envoi de la configuration à " + instal})
                    self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + instal)
                    i = 0
                    send_channel_message('cartcreating', {'message':'Attente que la carte ' + instal + ' se connecte'})
                    while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                            "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                        time.sleep(0.5)
                        print("wait again")
                        i += 1
                    if i == 1200:
                        print("La carte " + instal + " ne s'est pas connecté en 10 min")
                    else:
                        print("La carte " + instal + " est connectée")
                        send_channel_message('cartcreating', {'message':"La carte " + instal + " est connectée"})
                        time.sleep(2)
                        self.save_csv_configuration(path_csv=path_csv)

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Erreur: " + str(exc_type) + str(
                    fname) + str(exc_tb.tb_lineno) + str(ex)})
            self.close()

        if SC_TEST and installed_connecting:
            send_channel_message('cartcreating', {
                    'message': "<i class='fas fa-times' style='color: #fe0101;'></i> L'installation est encore en ligne. Pour ne pas écraser la configuration, veuillez faire les paramètres en local."})
            self.close()


    def savekey_installation(self, installation, dict_schematic):
        """
        1. Enregistre toutes les informations installateur, propriétaire, localisation
        :param installation: SN de l'installation SC2M...
        :param dict_schematic: json schémateque converti en dict python
        :return:
        """
        try:
            self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id='+installation)
            i = 0
            send_channel_message('cartcreating', {'message':'Attente '+ installation +' que la carte se connecte'})
            while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                    "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                time.sleep(0.5)
                print("wait again")
                i += 1
            if i == 1200:
                send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> La carte "+installation+" ne s'est pas connecté en 10 min"})
                self.close()
            else:
                send_channel_message('cartcreating', {'message':'La carte ' + installation + ' est connectée'})
                assert self.driver.find_element(By.XPATH, '//label[@for="input-pages-info"]')
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//label[@for="input-pages-info"]').click()
                time.sleep(2)
                self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-suivi"]').click()
                self.driver.find_element(By.ID, 'mail-defaut-adresses-solisart').send_keys("sav@solisart.fr")
                if 'formulaire' in dict_schematic:
                    dict_schematictemp = dict_schematic['formulaire']
                else:
                    dict_schematictemp = dict_schematic
                if "adresse_mail" in dict_schematictemp:
                    self.driver.find_element(By.ID, 'mail-defaut-adresses-installateur').\
                        clear()
                    print(dict_schematictemp['adresse_mail'])
                    self.driver.find_element(By.ID, 'mail-defaut-adresses-installateur'). \
                        send_keys(dict_schematictemp['adresse_mail'])
                if "installateur" in dict_schematictemp:
                    self.driver.find_element(By.ID, 'input-suivi-installateur'). \
                        clear()
                    self.driver.find_element(By.ID, 'input-suivi-installateur').\
                        send_keys(dict_schematictemp['installateur'])

                self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-client"]').click()
                for key, value in {
                    "prenom_client": 'input-client-prenom',
                    "nom_client": 'input-client-nom',
                    "mail_client": 'input-client-email',
                    "tel_client": 'input-client-telephone1'
                }.items():
                    if key in dict_schematictemp:
                        self.driver.find_element(By.ID, value). \
                        clear()
                        self.driver.find_element(By.ID, value).\
                        send_keys(dict_schematictemp[key])

                self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-localisation"]').click()
                for key, value in {
                    "adresse_client":'input-adresse-voie1',
                    "code_postale_client": 'input-adresse-codepostal',
                    "ville_client": 'input-adresse-commune'
                }.items():
                    if key in dict_schematictemp:
                        self.driver.find_element(By.ID, value). \
                            clear()
                        self.driver.find_element(By.ID, value). \
                            send_keys(dict_schematictemp[key])

                try:

                    url = 'https://api-adresse.data.gouv.fr/search/?q=' + dict_schematictemp['adresse_client'] +'&postcode='+ dict_schematictemp["code_postale_client"] + '&type=street'
                    import requests
                    resp = requests.get(url).json()
                    coordonnee=resp['features'][0]['geometry']['coordinates']
                    GPS=str(coordonnee[1])+ ','+str(coordonnee[0])

                    # url = 'https://nominatim.openstreetmap.org/?q=France'
                    # for at in ["adresse_client", "code_postale_client", "ville_client"]:
                    #     if at in dict_schematictemp:
                    #         url += '+' + dict_schematictemp[at].replace(' ', '%').replace('\'', '%').lower()
                    # url += '&format=json'
                    # import requests
                    # resp = requests.get(url).json()
                    # if not resp or not 'lon' in resp[0]:
                    #     GPS = None
                    #     pass
                    # else:
                    #     GPS = resp[0]['lat'] + ',' + resp[0]['lon']

                    if GPS == '46.603354,1.8883335':
                        GPS = None
                    if GPS:
                        self.driver.find_element(By.ID, 'input-adresse-gps'). \
                            send_keys(GPS)

                except Exception as ex:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(ex)
                    send_channel_message('cartcreating', {'message':'Les informations GPS pour' + installation + ' ne sont pas enregistrées'})

            self.driver.find_element(By.XPATH, '//a[@href="#onglet-enregistrement"]').click()
            self.driver.find_element(By.ID, 'button-enregistrement-enregistrer').click()
            send_channel_message(
                'cartcreating',{'message':"<i class='fas fa-check' style='color: #018303;'></i> Les informations pour " + installation + " sont bien enregistrées."}
            )
        except Exception as ex:
            send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ "ligne:" + str(exc_tb.tb_lineno) + str(ex) })
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Les informations sur l'installation et le propriétaire n'ont pas pu être enregistré."})


    def cart_created_since_json(self, kwargs):
        self.json_installation = True
        try:
            import requests
            installation = kwargs['installation']
            dict_schematic = kwargs['dict_schematic']
            CL = kwargs['CL']
            send_channel_message('cartcreating',
                                 {'message': "Recherche si l'installation " + installation + " existe déjà..."})
            list_install = self.list_installation()
            if installation in list_install:
                send_channel_message('cartcreating',
                                     {'message':"L'installation " + installation + " existe déjà! Fin du processus"})
                self.close()
            else:
                send_channel_message('cartcreating',
                                     {'message': "L'installation " + installation + " est bien à créer"})
                import os
                from django.core.files.storage import FileSystemStorage

                # Supprime tous les fichiers du dossier temp
                files = glob.glob(os.path.join(os.path.dirname(__file__), 'temp'))
                for f in files:
                    try:
                        os.remove(f)
                    except:
                        pass

                # Créer config.csv depuis le json
                from .convertjson import convertjson
                convertjson.jsontocsv(
                    installation_SN=installation, 
                    installation_name=dict_schematic['formulaire']['nom_client'].upper(),
                    path=os.path.join(os.path.dirname(__file__), 'temp', 'config.csv'),
                    dicttoconvert=dict_schematic
                    )


                send_channel_message('cartcreating',
                                     {
                                         'message': "<i class='fas fa-check' style='color: #018303;'></i> Le fichier .csv de configuration de l'installation " + installation + " a bien été créé",
                                         'download':"config"
                                     })

                from PIL import Image
                from io import BytesIO, StringIO

                # URL de l'api
                url = 'https://www.solisart.fr/schematics/api/getSchema.php?image=SchemaHydrauWithLegend'
                # ici getSchema.php peut contenir 2 paramètre get :
                #   -image : qui permet d'indiquer l'image à récupérer (SchemaHydrau, SchemaHydrauWithLegend, SchemaExe, Etiquetage, ImageFicheProg)
                #   -format : qui peut uniquement prendre la valeur PDF pour indiquer de renvoyer l'image en format PDF
                # exemple d'url pour récupérer l'etiquetage en format pdf :
                #   https://www.solisart.fr/schematics/api/getSchema.php?image=Etiquetage&format=PDF
                # dans le cas ou format n'est pas indiqué alors le téléchargement se fait en png

                # URL du fichier json qui sera envoyé
                # le fichier json doit être une configuration téléchargé depuis la schématèque
                # il peut être dans un ancien format cela ne devrait pas poser de problème

                # le fichier doit bien être passé avec l'identifiant 'fichier' sinon cela ne marchera pas

                # la requête doit passé obligatoirement le fichier en paramètre files
                response = requests.post(url, files={'fichier': json.dumps(dict_schematic)})

                # Lire les données de l'image depuis la réponse
                image_data = response.content
                #
                # # Créer une image à partir des données
                image = Image.open(BytesIO(image_data))

                import os
                # Sauvegarder dans le dossier /temp
                image.save(os.path.join(os.path.dirname(__file__), 'temp', 'image.png'))

                send_channel_message('cartcreating',
                                     {
                                         'message': "<i class='fas fa-check' style='color: #018303;'></i> L'image .png sur schéma hydro de l'installation " + installation + " a bien été créée"})
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ "ligne:" + str(exc_tb.tb_lineno) + str(ex) })
            self.close()

        self.cart_created_since_csv_config(path_csv = os.path.join(os.path.dirname(__file__), 'temp', 'config.csv'))

        if self.connecting:
            self.savekey_installation(installation, dict_schematic)
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Les informations sur l'installation et le propriétaire n'ont pas pu être enregistré."})

        if self.connecting:
            self.record_png(installation)
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le schéma de l'installation n'a pas pu être affecté"})

        created=False
        if self.connecting:
            created = self.createuser(dict_schematic)
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être créé."})

        if self.connecting and created:
            self.linkproprio(dict_schematic, installation)
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être affecté."})

        #Affecte CL 
        if not CL and 'fiche_prog' in dict_schematic:
            if 'numCommande' in dict_schematic['fiche_prog']:
                CL=dict_schematic['fiche_prog']['numCommande']
        install = installation
        if self.connecting and CL:
            try:
                CLf = CL_herakles.objects.get(CL = CL)
                CLf.date_prepa_carte = timezone.now().date()
                from .models import installation
                CLf.installation = installation.objects.get(idsa=install)
                CLf.save()
                send_channel_message('cartcreating',
                                     {
                                         'message': "<i class='fas fa-check' style='color: #018303;'></i> Le CL est affecté à l'installation."})
                 
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(ex)
                send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le CL n'a pas pu être affecté à l'installation."})
                send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ "ligne:" + str(exc_tb.tb_lineno) + str(ex) })
            
            try:                    
                commercial = CL_herakles.objects.get(CL = CL).commercial
                if commercial == "NONGLA":
                    self.acces_installation('NONGLATON', install, '2')
                elif commercial == "DURAND":
                    self.acces_installationl('DURAND', install, '2')
                elif commercial == "FOISSEY":
                    self.acces_installation('FOISSEY', install, '2')
                elif commercial == "CLAVAREAU":
                    self.acces_installation('techniconsultant.cc@orange.fr', install, '2')  
                send_channel_message('cartcreating',
                                     {
                                         'message': "<i class='fas fa-check' style='color: #018303;'></i> Le commercial " + str(commercial) +" a été affecté à l'installation"})
                
                     
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(ex)
                send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le commercial n'a pas pu être affecté à l'installation."})
                send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ "ligne:" + str(exc_tb.tb_lineno) + str(ex) })

            from .models import profil_user
            if 'formulaire' in dict_schematic:
                email_installateur = dict_schematic['formulaire']['adresse_mail']
            else:
                email_installateur = dict_schematic['adresse_mail']

            for email in list(profil_user.objects.filter(user__email=email_installateur).values_list('user__email', flat=True)):
                self.acces_installation(email, installation, '3')

        if self.connecting:
            send_channel_message('cartcreating',
                             {
                                 'message': "<i class='fas fa-check' style='color: #018303;'></i> La carte est complètement prête"})
            send_channel_message('cartcreating',
                             {
                                 'message': "<i class='fas fa-check' style='color: #018303;'></i><a href='https://my.solisart.fr/admin/?page=installation&id="+ install+"' target='_blank'>Visualiser l'installation "+ installation+ " créée</a>"})
            self.close()
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> La carte n'est pas complètement prête."})
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i><a href='https://my.solisart.fr/admin/?page=installation&id="+ install +"' target='_blank'>Visualiser l'installation "+ installation+ " créée</a>"})
            self.close()


    def linkproprio(self, dict_schematic, installation):

        if 'formulaire' in dict_schematic:
            dict_schematic = dict_schematic['formulaire']
        try:
            if dict_schematic['mail_client']:
                self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id='+installation)
                i = 0
                send_channel_message('cartcreating', {'message':'Attente '+ installation +' que la carte se connecte'})
                while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                    "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                    time.sleep(0.5)
                    print("wait again")
                    i += 1
                if i == 1200:
                    send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> La carte "+installation+" ne s'est pas connecté en 10 min"})
                    self.close()
                else:
                    time.sleep(3)
                    self.waitelement(By.XPATH, '//label[@for="input-pages-acces"]', 'presence_of_element_located', 'click')
                    self.waitelement(By.XPATH, '//a[@href="#onglet-acces-ajout-utilisateur"]', 'presence_of_element_located', 'click')
                    self.waitelement(By.XPATH, '//option[@value="'+dict_schematic['mail_client']+'"]', 'presence_of_element_located', 'click')
                    self.waitelement(By.XPATH, '//option[@value="4"]', 'presence_of_element_located', 'click')
                    self.waitelement(By.ID, 'acces-utilisateur-ajouter', 'presence_of_element_located', 'click')
                    send_channel_message('cartcreating',
                                    {
                                        'message': "<i class='fas fa-check' style='color: #018303;'></i> Le propriétaire a été affecté à l'installation"})
            else:
                send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Pas assez d'information pour créer le propriétaire"})
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating',
                                 {'message': "Erreur: " + str(exc_type) + str(fname) + str(exc_tb.tb_lineno) + str(ex)})
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être affecté."})

    def acces_installation(self, idsa, installation, level):

        try:
            self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id='+installation)
            i = 0
            send_channel_message('cartcreating', {'message':'Attente '+ installation +' que la carte se connecte'})
            while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                time.sleep(0.5)
                print("wait again")
                i += 1
            if i == 1200:
                send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> La carte "+installation+" ne s'est pas connecté en 10 min"})
                self.close()
            else:
                time.sleep(3)
                self.waitelement(By.XPATH, '//label[@for="input-pages-acces"]', 'presence_of_element_located', 'click')
                time.sleep(2)
                self.waitelement(By.XPATH, '//a[@href="#onglet-acces-ajout-utilisateur"]', 'presence_of_element_located', 'click')
                time.sleep(2)
                self.waitelement(By.XPATH, '//option[@value="'+ idsa +'"]', 'presence_of_element_located', 'click')
                self.waitelement(By.XPATH, '//option[@value="'+ str(level) +'"]', 'presence_of_element_located', 'click')
                self.waitelement(By.ID, 'acces-utilisateur-ajouter', 'presence_of_element_located', 'click')
                send_channel_message('cartcreating',
                                 {
                                     'message': "<i class='fas fa-check' style='color: #018303;'></i> Le propriétaire a été affecté à l'installation"})

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating',
                                 {'message': "Erreur: " + str(exc_type) + str(fname) + str(exc_tb.tb_lineno) + str(ex)})
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> "+ idsa +" n'a pas pu être affecté."})
            self.close()

    def record_png(self, installation):

        try:
            self.waitelement(By.XPATH, '//label[@for="input-pages-visualisation"]', 'presence_of_element_located', 'click')
            self.waitelement(By.XPATH, '//a[@href="#onglet-maintenance"]', 'presence_of_element_located', 'click')
            self.waitelement(By.ID, "schema-ajouter", 'presence_of_element_located', 'click')
            print(os.path.dirname(__file__) + '/temp/image.png')
            self.driver.find_element(By.ID, "telechargement-schema-input-1").send_keys(os.path.join(os.path.dirname(__file__), 'temp', 'image.png'))
            self.waitelement(By.ID, "telechargement-schema-ajouter", 'element_to_be_clickable', 'click')
            send_channel_message('cartcreating',
                                 {
                                     'message': "<i class='fas fa-check' style='color: #018303;'></i> L'image .png sur schéma hydro de l'installation " + installation + " a bien été affectée à l'onglet visualisation"})

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating',
                                 {'message': "Erreur: " + str(exc_type) + str(fname) + str(exc_tb.tb_lineno) + str(ex)})
            send_channel_message('cartcreating',
                                 {'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le schéma de l'installation n'a pas pu être affecté"})
            

    def cart_created_since_csv_config(self, path_csv=None):
        """
        Configurer une carte à partir d'un fichier csv
        :param csv: path depuis le fichier csv
        :return:
        """

        send_channel_message('cartcreating',
                                 {
                                     'message':"Recherche de connexion de l'installation SC_TEST dans la liste des installations"
                                 })

        list_install = self.list_installation()
        if not 'SC_TEST' in list_install:
            send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Abandon de de recherche d'installation SC_TEST."})
            self.close()
        else:
            send_channel_message('cartcreating', {'message':"<i class='fas fa-check' style='color: #018303;'></i> SC_TEST dans la liste des installations"})
            self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=SC_TEST')
            i = 0
            send_channel_message('cartcreating', {'message':"Attente qu'une carte vierge en SC_TEST se connecte..."})
            while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                        "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                time.sleep(0.5)
                print("wait again")
                i += 1
  
            if i == 1200:
                print("La carte SC_TEST ne s'est pas connecté en 10 min")
                send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Pas de connection de SC_TEST en 10min."})
                self.close()              
            else:
                if self.connecting:
                    self.update_regul('SC_TEST')

                if self.connecting:
                    self.update_nano('SC_TEST')
                else:
                    send_channel_message('cartcreating', {
                        'message': "<i class='fas fa-times' style='color: #fe0101;'></i> La carte de régulation n'a pas pu être mise à jour."})
                        
                if self.connecting:
                    send_channel_message('cartcreating',
                                         {'message': "Préparation de l'envoi de la configuration à SC_TEST"})
                    
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//label[@for="input-pages-administration"]').click()
                    time.sleep(2)
                    import csv
                    file = open(path_csv)
                    csv_file = csv.reader(file, delimiter=";")
                    lines = list(csv_file)
                    installation = lines[3][2]
                    proprio = lines[4][2]
                    file.close()
                    self.driver.find_element(By.ID, 'input-admin-serveur-serie').clear()
                    self.driver.find_element(By.ID, 'input-admin-serveur-serie').send_keys(installation)
                    self.driver.find_element(By.ID, 'input-admin-serveur-id').clear()
                    self.driver.find_element(By.ID, 'input-admin-serveur-id').send_keys(proprio)
                    time.sleep(2)
                    self.driver.find_element(By.XPATH, '//a[@href="#onglet-enregistrement"]').click()
                    self.driver.find_element(By.ID, 'button-enregistrement-enregistrer').click()
                    send_channel_message(
                        'cartcreating',{'message':"<i class='fas fa-check' style='color: #018303;'></i> Les informations pour " + installation + " sont bien enregistrées."}
                    )
                    self.save_csv_configuration(path_csv=path_csv)
                else:
                    send_channel_message('cartcreating', {
                        'message': "<i class='fas fa-times' style='color: #fe0101;'></i> La nano carte n'a pas pu être mise à jour."})

        if not self.json_installation:
            send_channel_message('cartcreating',
                                 {
                                     'message': "<i class='fas fa-check' style='color: #018303;'></i> La carte est terminée."})
            self.close()

    def update_regul(self, installation):
        try:
            self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + installation)
            send_channel_message('cartcreating', {'message':'Attente que la carte '+ installation +' se connecte'})
            self.waitelement(By.XPATH, '// *[@id="comm-statut"][@src="image/bullet_green.png"]', 'presence_of_element_located', '', time_max=1200)

            send_channel_message('cartcreating', {'message':"L'installation " +installation + ' est connectée'})
            time.sleep(2)
            self.waitelement(By.XPATH, '//label[@for="input-pages-maj"]', 'presence_of_element_located', 'click')
            time.sleep(2)
            self.waitelement(By.XPATH, '//a[@href="#onglet-carte"]', 'presence_of_element_located', 'click')
            time.sleep(2)            
            self.driver.find_element(By.ID, "firmware-nouveau-button").click()
            #clique sur la dernier màj
            ul = self.driver.find_element(By.ID, "firmware-nouveau-menu")
            ul.find_elements(By.TAG_NAME, 'li')[2].click()
            #Valide la màj
            self.waitelement(By.ID, "firmware-installer", 'presence_of_element_located', 'click')
            #Ferme la fenêtre de message
            time.sleep(2)
            self.waitelement(By.XPATH, '/html/body/div[2]/div[1]/button','presence_of_element_located','click')
            time.sleep(2)
            div = self.driver.find_element(By.ID, "firmware-maj")
            i = 0
            print("wait update")
            send_channel_message('cartcreating', {'message':"La carte de régulation de l'installation " +installation + ' en cours de mise à jour'})
            time.sleep(2)

            self.waitelement(By.XPATH,'//*[@id="firmware-maj"]/table/tbody/tr[2]/td[2]/img[@alt="Terminée avec succès"]',
                                 'presence_of_element_located', '', time_max=1200)

            send_channel_message('cartcreating',
                                     {'message':"<i class='fas fa-check' style='color: #018303;'></i> La carte de régulation de l'installation " + installation + ' est à la dernière version'})
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ str(exc_tb.tb_lineno) + str(ex) })
            self.close()

    def update_nano(self, installation):
        try:
            self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + installation)
            self.waitelement(By.XPATH, '// *[@id="comm-statut"][@src="image/bullet_green.png"]',
                             'presence_of_element_located', '', time_max=1200)
            time.sleep(2)
            self.waitelement(By.XPATH, '//label[@for="input-pages-maj"]', 'presence_of_element_located', 'click')
            time.sleep(2)
            self.waitelement(By.XPATH, '//a[@href="#onglet-serveur"]', 'presence_of_element_located', 'click')
            time.sleep(2)
            if self.driver.find_element(By.ID, "appli-courant").get_attribute("innerHTML") != \
                self.driver.find_element(By.CLASS_NAME, "version").get_attribute("innerHTML"):
                self.driver.find_element(By.ID, "appli-nouveau-button").click()

                # clique sur la dernier màj
                ul = self.driver.find_element(By.ID, "appli-nouveau-menu")
                ul.find_elements(By.TAG_NAME, 'li')[2].click()
                # Valide la màj
                self.driver.find_element(By.ID, "appli-installer").click()
                time.sleep(3)
                # Ferme la fenêtre de message
                self.waitelement(By.XPATH, '//button[@title="Close"]', 'presence_of_element_located', 'click')
                self.waitelement(By.XPATH, '////*[@id="appli-installer"]', 'presence_of_element_located', 'click')
                send_channel_message('cartcreating',
                                    {
                                        'message': "Le nano serveur de l'installation " + installation + ' est en cours de mise à jour'})
                time.sleep(2)

                self.waitelement(By.XPATH, '//*[@id="appli-maj"]/table/tbody/tr[2]/td[2]/img[@alt="Terminée avec succès"]',
                                    'presence_of_element_located', '', time_max=1200)
            print("Le nano-serveur est à la dernière version")
            send_channel_message('cartcreating',
                                 {
                                     'message': "<i class='fas fa-check' style='color: #018303;'></i> Le nano server de l'installation " + installation + ' est à la dernière version'})

        except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(ex)
                send_channel_message('cartcreating', {'message':"Erreur: " + str(exc_type) + str(fname)+ str(exc_tb.tb_lineno) + str(ex) })
                self.close()

    def downloadConfigCsvInstallation(self, installation):

        import os
        import glob
        files = glob.glob(get_download_path() + "\*.csv")
        for f in files:
            try:
                os.remove(f)
            except:
                pass

        self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + installation)
        send_channel_message('cartcreating',
                             {'message':"Connexion à l'installation: " + installation })
        time.sleep(2)
        self.waitelement(By.XPATH, '//label[@for="input-pages-maj"]','presence_of_element_located', 'click')
        time.sleep(2)
        self.waitelement(By.XPATH, '//a[@href="#onglet-config"]', 'presence_of_element_located','click')
        self.waitelement(By.ID, "bouton-sauvegarder", 'presence_of_element_located','click')
        time.sleep(2)
        self.waitelement(By.XPATH, '//*[@id="liste-configs"]/table/tbody/tr[2]/td[4]/a[2]', 'presence_of_element_located','click')
        send_channel_message('cartcreating',
                             {
                                 'message':"La configuration de l'installation "+ installation+" vient d'être téléchargée."
                             })
        #le fichier ce trouve dans le dossier télécharger et on le déplace dans temp
        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'temp', 'config.csv'))
        except:
            print("çà casse")
            pass

        try:
            os.rename(glob.glob(get_download_path() + "/*.csv")[0], os.path.join(os.path.dirname(__file__), 'temp', 'config.csv'))
            send_channel_message('cartcreating',
                                 {
                                     'download': "-"
                                 })

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Erreur: " + str(exc_type) + str(
                    fname) + str(exc_tb.tb_lineno) + str(ex)})
            self.close()
        self.cart_created_since_csv_config(os.path.join(os.path.dirname(__file__), 'temp', 'config.csv'))

    def createuser(self, dict_schematic):
        try:
            if 'formulaire' in dict_schematic:
                dict_schematic=dict_schematic['formulaire']
            if 'mail_client' in dict_schematic:
                self.driver.get('https://my.solisart.fr/admin/index.php?page=creer_utilisateur')
                if not dict_schematic['prenom_client']:
                    dict_schematic['prenom_client'] = '-'
                for key, value in {
                    "prenom_client": 'prenom',
                    "nom_client": 'nom',
                    "mail_client": 'email',
                    "tel_client": 'telephone1',
                    "adresse_client": 'voie1',
                    "code_postale_client": 'codepostal',
                    "ville_client": 'commune',
                    "mail_client": 'id',
                }.items():
                    if key in dict_schematic:
                        self.driver.find_element(By.XPATH, '//input[@name="'+ value +'"]'). \
                            clear()
                        self.driver.find_element(By.XPATH, '//input[@name="'+ value +'"]'). \
                            send_keys(dict_schematic[key])
                self.driver.find_element(By.XPATH, '//input[@name="pass_saisie"]'). \
                    clear()
                self.driver.find_element(By.XPATH, '//input[@name="pass_saisie"]'). \
                    send_keys('solaire')
                self.driver.find_element(By.XPATH, '//input[@name="pass_confirm"]'). \
                    clear()
                self.driver.find_element(By.XPATH, '//input[@name="pass_confirm"]'). \
                    send_keys('solaire')
                self.driver.find_element(By.XPATH, '//input[@name="creation"]'). \
                    click()
                send_channel_message('cartcreating', {'message':"<i class='fas fa-check' style='color: #018303;'></i> Le propriétaire "+ \
                    dict_schematic['prenom_client']+ \
                    " " + \
                    dict_schematic['nom_client'] + \
                    " a correctement été enregistré."})
                return True
            else:
                send_channel_message(
                    'cartcreating',
                    {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être créé."}
                )
                return False
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Erreur: " + str(exc_type) + str(
                    fname) + str(exc_tb.tb_lineno) + str(ex)})
            send_channel_message(
                    'cartcreating',
                    {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être créé."}
                )
            return False

