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
        return os.path.join(os.path.expanduser('~'), 'downloads')

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
            # if not os.name =='nt':
            #     from selenium import webdriver
            #     from selenium.webdriver.firefox.service import Service as FirefoxService
            #     from webdriver_manager.firefox import GeckoDriverManager
            #
            #     self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            # else:
            #     from selenium import webdriver
            #     from selenium.webdriver.firefox.service import Service
            #     service = Service(
            #         executable_path=r"C:\Users\freddy\Downloads\geckodriver-v0.32.0-win32\geckodriver.exe"
            #     )
            #     self.driver = webdriver.Firefox(
            #         service=service
            #     )
            from selenium import webdriver
            from selenium.webdriver.firefox.service import Service as FirefoxService
            from webdriver_manager.firefox import GeckoDriverManager
            from selenium.webdriver import FirefoxOptions
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=opts)
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
            wait = WebDriverWait(self.driver, time_max)
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

        install = self.waitelement(By.XPATH, '//*[@class="liste_colonne_paire"]/a[2]', 'presence_of_all_elements_located', None)

        return [i.get_attribute("innerHTML") for i in install]
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
            self.driver.find_element(By.ID, "upload-input-3").send_keys(path_csv.replace('\\', '\\\\').replace('/', '\\\\'))
            time.sleep(2)
            self.driver.find_element(By.ID, "bouton-telecharger").click()
            time.sleep(3)
            self.driver.find_element(By.XPATH, '//*[@id="liste-configs"]/table/tbody/tr[2]/td[4]/a[1]').click()
            self.waitelement(By.XPATH, '//button[@title="Close"]', 'presence_of_element_located', 'click')
            time.sleep(10)
            try:
                self.driver.find_element(By.XPATH, '//a[@href="#onglet-enregistrement"]').click()
                time.sleep(2)
                self.driver.find_element(By.ID, 'button-enregistrement-enregistrer').click()
                send_channel_message('cartcreating', {'message':"<i class='fas fa-check' style='color: #018303;'></i> Configuration de l'installation " + installation + " sauvegardée"})
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(ex)
                send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Aucune modification n'a été détecté pour l'installation " + installation})


            #to do ajouter si install n'est pas en ligne
            if self.driver.current_url == 'https://my.solisart.fr/admin/index.php?page=installation&id=SC_TEST':
                SC_TEST = True
            else:
                SC_TEST = False
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
                while i < 10 and not installation in l:
                    i += 1
                    l = self.list_installation()
                if i == 10:
                    send_channel_message('cartcreating', {'message':"<i class='fas fa-times' style='color: #fe0101;'></i> Abandon de de recherche d'installation " + installation})
                    self.close()
                else:
                    send_channel_message('cartcreating', {'message':'<i class="fas fa-check" style="color: #018303;"></i> Installation ' + installation + " dans la liste des installations"})
                    send_channel_message('cartcreating', {'message':"Préparation de l'envoi de la configuration à " + installation})
                    self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id=' + installation)
                    i = 0
                    send_channel_message('cartcreating', {'message':'Attente que la carte ' + installation + ' se connecte'})
                    while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                            "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
                        time.sleep(0.5)
                        print("wait again")
                        i += 1
                    if i == 1200:
                        print("La carte " + installation + " ne s'est pas connecté en 10 min")
                    else:
                        print("La carte " + installation + " est connectée")
                        send_channel_message('cartcreating', {'message':"La carte " + installation + " est connectée"})
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
        self.driver.get('https://my.solisart.fr/admin/index.php?page=installation&id='+installation)
        i = 0
        send_channel_message('cartcreating', 'Attente '+ installation +' que la carte se connecte')
        while self.driver.find_element(By.ID, 'comm-statut').get_attribute(
                "src") != 'https://my.solisart.fr/admin/image/bullet_green.png' and i < 1200:
            time.sleep(0.5)
            print("wait again")
            i += 1
        if i == 1200:
            send_channel_message('cartcreating', "<i class='fas fa-times' style='color: #fe0101;'></i> La carte "+installation+" ne s'est pas connecté en 10 min")
            self.close()
        else:
            send_channel_message('cartcreating', 'La carte ' + installation + ' est connectée')
            assert self.driver.find_element(By.XPATH, '//label[@for="input-pages-info"]')
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//label[@for="input-pages-info"]').click()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-suivi"]').click()

            self.driver.find_element(By.ID, 'mail-defaut-adresses-solisart').clean()
            self.driver.find_element(By.ID, 'mail-defaut-adresses-solisart').send_keys("sav@solisart.fr")
            if "adresse_mail" in dict_schematic:
                self.driver.find_element(By.ID, 'mail-defaut-adresses-installateur').\
                    clear()
                self.driver.find_element(By.ID, 'mail-defaut-adresses-installateur'). \
                    send_keys(dict_schematic['adresse_mail'])
            if "installateur" in dict_schematic:
                self.driver.find_element(By.ID, 'input-suivi-installateur'). \
                    clear()
                self.driver.find_element(By.ID, 'input-suivi-installateur').\
                    send_keys(dict_schematic['installateur'])

            self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-client"]').click()
            for key, value in {
                "prenom_client": 'input-client-prenom',
                "nom_client": 'input-client-nom',
                "mail_client": 'input-client-email',
                "tel_client": 'input-client-telephone1'
            }.items():
                if key in dict_schematic:
                    self.driver.find_element(By.ID, value). \
                    clear()
                    self.driver.find_element(By.ID, value).\
                    send_keys(dict_schematic[key])

            self.driver.find_element(By.XPATH, '//a[@href="#onglet-info-localisation"]').click()
            for key, value in {
                "adresse_client":'input-adresse-voie1',
                "code_postale_client": 'input-adresse-codepostal',
                "ville_client": 'input-adresse-commune'
            }.items():
                if key in dict_schematic:
                    self.driver.find_element(By.ID, value). \
                        clear()
                    self.driver.find_element(By.ID, value). \
                        send_keys(dict_schematic[key])

            try:
                url = 'https://nominatim.openstreetmap.org/?q=France'
                for at in ["adresse_client", "code_postale_client", "ville_client"]:
                    if at in dict_schematic:
                        url += '+' + dict_schematic[at].replace(' ', '%').replace('\'', '%').lower()
                url += '&format=json'
                import requests
                resp = requests.get(url).json()
                if not resp or not 'lon' in resp[0]:
                    GPS = None
                    pass
                else:
                    GPS = resp[0]['lat'] + ',' + resp[0]['lon']

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
                send_channel_message('cartcreating', 'Les informations pour' + installation + ' ne sont pas enregistrées')
        self.driver.find_element(By.XPATH, '//a[@href="#onglet-enregistrement"]').click()
        self.driver.find_element(By.ID, 'button-enregistrement-enregistrer').click()
        send_channel_message(
            'cartcreating',
            "<i class='fas fa-check' style='color: #018303;'</i> Les informations pour" + installation + " sont bien enregistrées"
        )

    def cart_created_since_json(self, kwargs):
        self.json_installation = True
        try:
            import requests
            installation = kwargs['installation']
            dict_schematic = kwargs['dict_schematic']
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
                files = glob.glob(os.path.dirname(__file__) + '/temp')
                for f in files:
                    try:
                        os.remove(f)
                    except:
                        pass

                # url pour récupérer la confi.csv depuis le json
                url = 'https://www.solisart.fr/schematics/api/getConfiguration.php'
                response = requests.post(url, files = {'fichier': json.dumps(dict_schematic)})
                # Ecrit le fichier config dans le dossier tmp
                with open(os.path.dirname(__file__) + '/temp/configtmp.csv', 'w') as out:
                    out.write(response.content.decode())
                import csv
                open_file = open(os.path.dirname(__file__) + '/temp/configtmp.csv')
                csv_file = csv.reader(open_file, delimiter=";")
                lines = list(csv_file)

                lines[3][2]=installation
                lines[4][2] = dict_schematic['formulaire']['nom_client'].upper()
                with open(os.path.dirname(__file__) + '/temp/config.csv', 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerows(lines)

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
                # SAuvegarder dans le dossier /temp
                image.save(os.path.dirname(__file__) + '/temp/image.png')

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

        self.cart_created_since_csv_config(path_csv=os.path.dirname(__file__) + '/temp/config.csv')

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
            self.linkproprio(dict_schematic)
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> Le propriétaire n'a pas pu être affecté."})
        if self.connecting:
            send_channel_message('cartcreating',
                             {
                                 'message': "<i class='fas fa-check' style='color: #018303;'></i> La carte est complètement prête"})
            self.close()
        else:
            send_channel_message('cartcreating', {
                'message': "<i class='fas fa-times' style='color: #fe0101;'></i> La carte n'est pas complètement prête."})


    def linkproprio(self, dict_schematic):
        try:
            self.waitelement(By.XPATH, '//label[@for="input-pages-acces"]', 'presence_of_element_located', 'click')
            self.waitelement(By.XPATH, '//a[@href="#onglet-acces-ajout-utilisateur"]', 'presence_of_element_located', 'click')
            self.waitelement(By.XPATH, '//option[@value="'+dict_schematic['mail_client']+'"]', 'presence_of_element_located', 'click')
            self.waitelement(By.XPATH, '//option[@value="4"]', 'presence_of_element_located', 'click')
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
            self.close()

    def record_png(self, installation):

        try:
            self.waitelement(By.XPATH, '//label[@for="input-pages-visualisation"]', 'presence_of_element_located', 'click')
            self.waitelement(By.XPATH, '//a[@href="#onglet-maintenance"]', 'presence_of_element_located', 'click')
            self.waitelement(By.ID, "schema-ajouter", 'presence_of_element_located', 'click')
            self.driver.find_element(By.ID, "telechargement-schema-input-1").send_keys(os.path.dirname(__file__) + '/temp/image.png')
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
            self.close()

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

            print("La carte de régulation est à la dernière version")
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
            self.driver.find_element(By.ID, "appli-nouveau-button").click()

            # clique sur la dernier màj
            ul = self.driver.find_element(By.ID, "appli-nouveau-menu")
            ul.find_elements(By.TAG_NAME, 'li')[2].click()
            # Valide la màj
            self.driver.find_element(By.ID, "appli-installer").click()
            time.sleep(3)
            # Ferme la fenêtre de message
            self.waitelement(By.XPATH, '//button[@title="Close"]', 'presence_of_element_located', 'click')
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
            os.remove(os.path.dirname(__file__) + '/temp/config.csv')
        except:
            print("çà casse")
            pass


        os.rename(glob.glob(get_download_path() + "/*.csv")[0], os.path.dirname(__file__) + '/temp/config.csv')
        send_channel_message('cartcreating',
                             {
                                 'download': "-"
                             })
        self.cart_created_since_csv_config(path_csv=os.path.dirname(__file__) + '/temp/config.csv')

    def createuser(self, dict_schematic):

        if 'mail_client' in dict_schematic:
            self.driver.get('https://my.solisart.fr/admin/index.php?page=creer_utilisateur')
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
            # self.driver.find_element(By.XPATH, '//input[@name="creation"]'). \
            #     click()
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

