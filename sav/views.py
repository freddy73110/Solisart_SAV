# -*- coding: utf-8 -*-
import json
import os
import sys

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views import View
from .forms import *
from .models import *

import pandas as pd
import numpy as np


class home (View):
    login_url = '/login/'
    template_name = 'sav/home.html'
    title = 'Recherche'

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )

    def post(self, request, *args, **kwargs):
        if 'id_instal' in request.POST :
            table_list=installation.objects.filter(idsa__icontains=request.POST['id_instal'])
            return render(request,
                      'widgets/table_recherche.html',
                      {
                          'utilisateurs': [],
                          'table': table_list
                      }
                      )
        if 'telephone' in request.POST:
            installation_list = installation.objects.all()
            utilisateurs = User.objects.all()
            if request.POST['telephone']:
                utilisateurs=utilisateurs.filter(Q(profil_user__telephone1__icontains=request.POST['telephone'])|Q(profil_user__telephone2__icontains=request.POST['telephone']))
                installation_list=installation_list.filter(
                    Q(acces__utilisateur__profil_user__telephone1__icontains=request.POST['telephone'])| \
                    Q(acces__utilisateur__profil_user__telephone2__icontains=request.POST['telephone']))
            if request.POST['prenom']:
                utilisateurs = utilisateurs.filter(first_name__icontains=request.POST['prenom'])
                installation_list=installation_list.filter(acces__utilisateur__first_name__icontains=request.POST['prenom'])
            if request.POST['nom']:
                utilisateurs = utilisateurs.filter(last_name__icontains=request.POST['nom'])
                installation_list = installation_list.filter(acces__utilisateur__last_name__icontains=request.POST['nom'])
            if request.POST['email']:
                utilisateurs = utilisateurs.filter(email__icontains=request.POST['email'])
                installation_list = installation_list.filter(acces__utilisateur__email__icontains=request.POST['email'])

            return render(request,
                      'widgets/table_recherche.html',
                      {
                          'utilisateurs': utilisateurs.distinct(),
                          'table': installation_list.distinct()
                      }
                      )

class updateDB (View):
    login_url = '/login/'
    form_class=updateDBForm
    template_name = 'sav/updateDB.html'
    title = 'Importation depuis my.solisart'

    def get(self, request, *args, **kwargs):

        return render(request,
                      self.template_name,
                      {
                          'title':self.title,
                          'form': self.form_class
                      }
                      )

    def post(self, request, *args, **kwargs):
        if 'submit' in request.POST:
            uploaded_file = request.FILES['fichier']
            df = pd.read_csv(uploaded_file, error_bad_lines=False, header=None)
            dictionary = {
                'Ã©': 'é',
                'Ã¨': 'è',
                'Ã«':'ë',
                'Ã§':'ç',
                'Ã§':'ï',
                'Ã´':'ô',
                'Ã ':'à',
                'Ã¢':'â',
                'Ãª':'ê',
                'Ã®':'î',
                '&#233;':'é',
                '&#234;': 'ê',
                '&#232;':'è',
                '&apos;': '\'',
                }
            df.replace(dictionary, regex=True, inplace=True)
            if 'utilisateur' in uploaded_file.name:
                print("avant", User.objects.all().count())
                df.columns=['id', 'pass', 'nom', 'prenom', 'email', 'telephone1', 'telephone2','voie1', 'voie2', 'voie3', 'codepostal', 'commune']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created=0
                for index, row in df.iterrows():
                    try:
                        user, created = User.objects.get_or_create(
                            username= row["email"] if row["email"] != np.nan else str(row['prenom']) + '.' + str(row['nom']),
                            first_name=row['prenom'],
                            last_name=row['nom'],
                            email=row["email"]
                        )
                        profil = profil_user.objects.get(user=user)
                        profil.idsa = row['id']
                        profil.PW = row['pass']
                        profil.telephone1 = row['telephone1'] if row['telephone1'].replace('.', '').replace(' ', '') != profil.telephone1 else profil.telephone1
                        profil.telephone2 = row['telephone2'] if row['telephone2'].replace('.', '').replace(' ', '') != profil.telephone2 else profil.telephone2
                        profil.voie1 =row['voie1']
                        profil.voie2 = row['voie2']
                        profil.voie3 = row['voie3']
                        profil.codepostal = row['codepostal']
                        profil.commune = row['commune']
                        profil.save()
                        if created:
                            total_created += 1

                    except:
                        pass
                print("après", User.objects.all().count())

                messages.success(request, str(total_created) + ' nouveaux utilisateur de créer')

            if 'profil' in uploaded_file.name:
                df.columns = ['id', 'nom', 'type', 'droit_gestion', 'droit_carte', 'icone']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        p_t, created = profil_type.objects.get_or_create(
                            name=row['nom'],
                            type=row['type'],
                            idsa=row['id']
                        )
                        if created:
                            total_created += 1


                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)

                    pass

                messages.success(request, str(total_created) + ' nouveaux profils type')

            if 'installation' in uploaded_file.name:
                df.columns = ['id', 'type_communication', 'version_carte_firmware', 'version_carte_interface',
                              'version_serveur_appli', 'heure_contact', 'heure_test', 'adresse_ip_wan',
                              'port_tcp_wan', '	propager_droits']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = installation.objects.get_or_create(
                            idsa=row['id'])
                        int.type_communication=row['type_communication'] if row['type_communication'] != np.nan else None,
                        int.version_carte_firmware=row['version_carte_firmware'] if row['version_carte_firmware'] != np.nan else None,
                        int.version_carte_interface=row['version_carte_interface'] if row['version_carte_interface'] != np.nan else None,
                        int.version_serveur_appli=row['version_serveur_appli'] if row['version_serveur_appli'] != np.nan else None,
                        int.adresse_ip_wan=row['adresse_ip_wan'] if row['adresse_ip_wan'] != np.nan else None,
                        int.port_tcp_wan=row['port_tcp_wan'] if row['port_tcp_wan'] != np.nan else None
                        int.save()

                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouvelles installations')

            if 'attribut_def' in uploaded_file.name:
                df.columns = ['id', 'description']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = attribut_def.objects.get_or_create(
                            idsa=row['id'],
                            description=row['description'] if row['description'] != np.nan else None
                        )
                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouvelles attribut_def')

            if 'attribut_val' in uploaded_file.name:
                df.columns = ['installation', 'attribut_def', 'valeur']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = attribut_valeur.objects.get_or_create(
                            installation=installation.objects.get(idsa=row['installation']),
                            attribut_def=attribut_def.objects.get(idsa=row['attribut_def'])
                        )
                        int.valeur=row['valeur']
                        int.save()
                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouvelles attribut_val')

            if 'acces' in uploaded_file.name:
                df.columns = ['utilisateur', 'profil', 'installation']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = acces.objects.get_or_create(
                            installation=installation.objects.get(idsa=row['installation']),
                            profil_type=profil_type.objects.get(idsa=row['profil']),
                            utilisateur=User.objects.get(profil_user__idsa=row['utilisateur'])
                        )
                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouveaux acces')

            if 'donnee' in uploaded_file.name:
                df.columns = ['id', 'nom_carte', 'nom','description', 'id_statut', 'droit_modification']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = donnee.objects.get_or_create(
                            idsa=row['id'],
                            nom_carte=row['nom_carte'],
                            description=row['description'] if row['description'] != np.nan else None
                        )
                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouvelles données')

            if 'historique' in uploaded_file.name:
                df.columns = ['installation', 'heure', 'donnee', 'valeur']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created = 0
                for index, row in df.iterrows():
                    try:
                        int, created = historique.objects.get_or_create(
                            installation=installation.objects.get(idsa=row['installation']),
                            donnee=donnee.objects.get(idsa=row['donnee'])
                        )
                        int.valeur = row['valeur']
                        int.save()
                        if created:
                            total_created += 1
                    except Exception as e:

                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(e)
                        pass

                messages.success(request, str(total_created) + ' nouveaux historiques')

        return render(request,
                      self.template_name,
                      {
                          'title':self.title,
                          'form': self.form_class
                      }
                      )

class installation_view (View):
    login_url = '/login/'
    template_name = 'sav/installation.html'
    title = 'Installation'

    def dispatch(self, request, *args, **kwargs):

        self.pk = kwargs.pop('pk')
        self.instal = installation.objects.get(pk=self.pk)
        self.attribut_val = attribut_valeur.objects.filter(installation=self.instal)
        self.liste_evenements=evenement.objects.filter(installation=self.instal).order_by('-date')
        self.add_ticket_form = ticket_form(installation=self.instal)
        self.add_evenement = add_evenement_form(user=request.user, installation=self.instal)
        self.add_problem = add_problem_form()
        self.form_class=installation_form(instance=self.instal)
        self.title = self.title + ' ' + str(self.instal) + ' / '
        self.title+= str(self.instal.proprio()) if self.instal.proprio() else ''
        self.histo= historique.objects.filter(installation=self.instal)
        return super(installation_view, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):



        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'instal': self.instal,
                          'liste_evenements': self.liste_evenements,
                          'attribut_val': self.attribut_val,
                          'histo': self.histo,
                          'add_evenement': self.add_evenement,
                          'add_ticket_form': self.add_ticket_form,
                          'add_problem_form': self.add_problem,
                          'form': self.form_class
                      }
                      )

    def post(self, request, *args, **kwargs):
        if "file_ticket" in request.POST:
            form = FilesForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save()
                tic = ticket.objects.get(pk=int(request.POST["file_ticket"]))
                tic.fichier.add(files)
                data = {'is_valid': True, 'name': files.fichier.name, 'url': files.fichier.url, 'file_id': files.id,
                        'size': files.fichier.size}
            else:
                data = {'is_valid': False}
            return JsonResponse(data, safe=False)

        elif "GPS_id" in request.POST:
            a = attribut_valeur.objects.get(pk=request.POST['GPS_id'])
            a.valeur = request.POST['CoordonneeGPS']
            a.save()
            data={"valide": "ok", "message": "Modifer avec succès"}
            return JsonResponse(data, safe=False)

        elif "details" in request.POST:
            t= ticket.objects.get(pk=int(str(request.POST['id']).replace('ta_ticket_', '')))
            t.detail=request.POST['details']
            t.save()
            return JsonResponse({
                "detail": "ok"
            }, safe=False)

        elif "submit" in request.POST:
            self.form_class=installation_form(request.POST, request.FILES, instance=self.instal)
            if self.form_class.is_valid():
                self.form_class.save()
                return HttpResponseRedirect(reverse('sav:installation', kwargs={'pk':int(self.instal.id)}))

        elif request.POST['nature_form'] == "add_problem":
            pb, created = probleme.objects.get_or_create(
                categorie=request.POST['categorie'],
                sous_categorie=request.POST['sous_categorie']
            )
            return JsonResponse({
                "probleme": {
                    "title": str(pb),
                    'id': pb.id
                }
            }, safe=False)

        elif request.POST['nature_form'] == "update-ticket":
            tick=ticket.objects.get(pk=int(request.POST['id']))
            add_ticket_form = ticket_form(request.POST, instance=tick)
            add_evenement = add_evenement_form(request.POST, instance=evenement.objects.get(ticket=tick),
                user=request.user,
                installation=self.instal)

            if add_evenement.is_valid():
                add_evenement.save()
            if add_ticket_form.is_valid():
                add_ticket_form.save()
            return JsonResponse({
                "update_ticket": "done"
            }, safe=False)

        elif request.POST['nature_form'] == "ticket":

            self.add_evenement = add_evenement_form(request.POST,user=request.user, installation=self.instal)
            if self.add_evenement.is_valid():
                even = self.add_evenement.save()
            self.add_ticket_form = ticket_form(request.POST, installation=self.instal)
            if self.add_ticket_form.is_valid():
                tick = self.add_ticket_form.save(commit=False)
                tick.evenement=even
                tick.save()
            return JsonResponse({
                "ticket": "ok"
            }, safe=False)

        elif request.POST['nature_form'] == "update_ticket_init":
            if request.POST['id']== '0':
                add_ticket_form = ticket_form(installation=self.instal)
                add_evenement = add_evenement_form(
                    user=request.user,
                    installation=self.instal)
            else:
                add_ticket_form=ticket_form(instance=ticket.objects.get(pk=int(request.POST['id'])),installation=self.instal)
                add_evenement=add_evenement_form(
                    instance=evenement.objects.get(ticket__pk=int(request.POST['id'])),
                    user=request.user,
                    installation=self.instal)

            return render(request,"widgets/crispy_form.html",
                          {'add_ticket_form': add_ticket_form,
                           'add_evenement':add_evenement})

        elif request.POST['nature_form'] == "delete_file":
            f=Fichiers.objects.get(pk=int(request.POST['delete_file_input'].replace('deletefile_', '')))
            file_name=f.fichier.name
            f.delete()
            return JsonResponse({
                "deleted":file_name
            }, safe=False)

        elif request.POST['nature_form'] == "rename_file":
            f = Fichiers.objects.get(pk=int(request.POST['rename_file_input'].replace('renamefile_', '')))
            f.titre=request.POST['new_name']
            f.save()
            return JsonResponse({
                "renamed": str(f)
            }, safe=False)

class utilisateur_view (View):
    login_url = '/login/'
    template_name = 'sav/utilisateur.html'
    form_class = UserForm
    title = 'utilisateur'

    def dispatch(self, request, *args, **kwargs):
        self.pk = kwargs.pop('pk')
        self.util = User.objects.get(pk=int(self.pk))
        self.profil=profil_user.objects.get(user=self.util)
        return super(utilisateur_view, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form_profil= ProfilForm(instance=self.profil)
        return render(request,
                      self.template_name,
                          {
                              'title': str(self.profil),
                              'util': self.util,
                              'profil': self.profil,
                              'form': self.form_class(instance=self.util),
                              'form_profil':form_profil
                          }
                      )

    def post(self, request, *args, **kwargs):
        if "modifier_profil" in request.POST:
            form_user = UserForm(request.POST, instance=self.util)
            form_profil = ProfilForm(request.POST, instance=self.profil)
            data={}
            if form_user.is_valid():
                form_user.save()
                data['user']='updated'
            if form_profil.is_valid():
                profil = form_profil.save()
                data['profil']='updated'
                try:
                    import requests
                    adresse = ''
                    if profil.voie1:
                        adresse += profil.voie1 + '%'
                    if profil.voie2:
                        adresse += profil.voie2 + '%'
                    if profil.codepostal:
                        adresse += profil.codepostal + '%'
                    if profil.commune:
                        adresse += profil.commune + '%'
                    url = 'https://nominatim.openstreetmap.org/?q=' + adresse + '&format=json&limit=1'
                    profil.longitude=requests.get(url).json()[0]['lon']
                    profil.latitude = requests.get(url).json()[0]['lat']
                    profil.save()
                except:
                    pass
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'data':'error'}, safe=False)




class carte (View):
    login_url = '/login/'
    template_name = 'sav/map.html'
    title = 'Répartition des installations'

    def dispatch(self, request, *args, **kwargs):
        return super(carte, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        test = attribut_valeur.objects.filter(attribut_def__description="Coordonnées GPS DD")\
                                    .exclude(valeur="nan")
        installateur = User.objects.filter(acces__profil_type__name='Installateur').distinct()

        return render(request,
                      self.template_name,
                          {
                              'title': self.title,
                              'test':test
                          }
                      )

    def post(self, request, *args, **kwargs):

        import requests
        url = 'https://nominatim.openstreetmap.org/?q=' + request.POST['adresse'].replace(' ', '%') + '&format=json&polygon_geojson=1'
        return HttpResponse(requests.get(url), content_type='application/json; charset=utf-8')

class ticket_view(View):
    login_url = '/login/'
    template_name = 'sav/ticket.html'
    title = 'Tickets ouverts'

    def get(self, request, *args, **kwargs):
        all_ticket_open=ticket.objects.exclude(etat=2)
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'all_ticket_open':all_ticket_open
                      }
        )


class bidouille (View):
    login_url = '/login/'
    template_name = 'sav/bidouille.html'
    title = 'Bidouille'

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )

