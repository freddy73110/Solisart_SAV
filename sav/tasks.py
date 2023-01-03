import datetime

from celery import shared_task
from django.core.files.base import ContentFile
from django.db.models.functions import Substr, Lower

from .models import profil_user, ticket, Fichiers, installation
import time
import io, os
from PIL import Image

@shared_task
def add(x, y):
    time.sleep(10)
    print(x, y)

    return str(x + y) + "Hello World"

@shared_task
def rapport_ticket():

    commerciaux = profil_user.objects.filter(departement__isnull=False)
    tickets =ticket.objects.filter(
        evenement__date__gte = datetime.date.today() - datetime.timedelta(days = 30),
        evenement__installation__attribut_valeur__attribut_def__description = "Code postal",
    )

    for commercial in commerciaux:
        #list des tickets par affectation commerciale
        tickets = ticket.objects.filter(
            evenement__date__gte=datetime.date.today() - datetime.timedelta(days=10),
            evenement__installation__attribut_valeur__attribut_def__description="Code postal",
        ).annotate(num_departement=Lower(Substr('evenement__installation__attribut_valeur__valeur', 1, 2))).filter(num_departement__in=list(commercial.departement))


    return None

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