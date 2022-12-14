# -*- coding: utf-8 -*-
import datetime
import io
import json
import os
import sys
import time
from datetime import timedelta
from email.mime.image import MIMEImage
from io import StringIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files import File
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Count, F, When, Value, Case, CharField, Func, Subquery, FloatField, OuterRef
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncHour, ExtractHour, ExtractDay, \
    ExtractWeekDay
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from plotly.subplots import make_subplots

from .forms import *
from .models import *

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.offline as opy

from imap_tools import MailBox, A, AND, OR, NOT

from email.mime.image import MIMEImage

from django.contrib.staticfiles import finders
from functools import lru_cache


@lru_cache()
def addimg(path, name):
    with open(path, 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data)
    logo.add_header('Content-ID', '<'+name+'>')
    return logo

class inbox():

    def mailbox(request):
        email_user = "sav@solisart.fr"
        email_pass = "AristideBerges218"
        server = 'imap.webmo.fr'

        return MailBox(server).login(email_user, email_pass)

    def mailbox_search(request, fetch=None):
        if not fetch:
            fetch = A(date_gte=(datetime.now() - timedelta(days=1)).date())
        else:
            fetch = A(fetch, date_gte=(datetime.now() - timedelta(days=3)).date())

        return inbox.mailbox(request).fetch(fetch)

    def fileattchment(msg):
        return [{'name':att.filename, 'type':att.content_type} for att in msg.attachments]
        # for att in msg.attachments:
        #     print(att.filename, att.content_type)
        #     with open('C:/1/{}'.format(att.filename), 'wb') as f:
        #         f.write(att.payload)

    def list(request, fetch=None):

        mailbox = inbox.mailbox_search(request, fetch=None)
        list_mail=[]
        for e in mailbox:
            try:
                icon = profil_user.objects.get(user__email=e.from_).icon()
                t_form = ticket_form(utilisateur=User.objects.get(email=e.from_), forme='email')
                e_form = add_evenement_form(user=request.user, user_acces=User.objects.get(email=e.from_), date=e.date)
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(ex)
                icon =''
                t_form=ticket_form(forme='email')
                e_form=add_evenement_form(user=request.user, date=e.date)
            list_mail.append({'date':e.date,
                                  'from_':e.from_,
                                  'subject':e.subject,
                                  'html':e.html,
                                  'text':e.text,
                                  'icon':icon,
                                  'uid':e.uid,
                                  # 'attachment': inbox.fileattchment(e),
                                  'ticket_form':t_form,
                                  'evenement_form':e_form,
                                    })
        return list_mail[::-1]

class home (View):
    login_url = '/login/'
    template_name = 'sav/home.html'
    title = 'Recherche'

    def get(self, request, *args, **kwargs):
        from .tasks import rapport_ticket
        rapport_ticket()

        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )

    def post(self, request, *args, **kwargs):
        if 'id_instal' in request.POST :
            table_list = installation.objects.all()
            if request.POST['ville_install']:
                table_list = table_list.filter(attribut_valeur__attribut_def__description="Commune",
                                               attribut_valeur__valeur__icontains=request.POST['ville_install'])
            if request.POST['code_postale_install']:
                table_list=table_list.filter(attribut_valeur__attribut_def__description="Code postal",
                                             attribut_valeur__valeur__icontains=request.POST['code_postale_install'])
            if request.POST['id_instal']:
                table_list=table_list.filter(idsa__icontains=request.POST['id_instal'])
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
                installation_list = (installation_list.filter(acces__utilisateur__last_name__icontains=request.POST['nom'])|\
                installation.objects.filter(idsa__icontains=request.POST['nom']) |\
                installation.objects.filter(attribut_valeur__valeur__icontains=request.POST['nom'])).distinct()
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
            df = pd.read_csv(uploaded_file, on_bad_lines='skip', header=None)
            dictionary = {
                '????': '??',
                '????': '??',
                '????':'??',
                '????':'??',
                '????':'??',
                '?? ':'??',
                '????':'??',
                '????':'??',
                '????':'??',
                '&#233;':'??',
                '&#234;': '??',
                '&#232;':'??',
                '&apos;': '\'',
                }
            df.replace(dictionary, regex=True, inplace=True)
            if 'utilisateur' in uploaded_file.name:
                df.columns=['id', 'pass', 'nom', 'prenom', 'email', 'telephone1', 'telephone2','voie1', 'voie2', 'voie3', 'codepostal', 'commune']
                df = df.reset_index()  # make sure indexes pair with number of rows
                total_created=0
                for index, row in df.iterrows():
                    try:
                        user, created = User.objects.get_or_create(
                            username = row["id"]
                        )
                        user.first_name = row['prenom'],
                        user.last_name = row['nom'],
                        user.email = row["email"]
                        #Comprend pas cette ligne mais ???? marche
                        user.first_name = user.first_name[0]
                        user.last_name = user.last_name[0]
                        user.save()
                        profil = profil_user.objects.get(user=user)
                        profil.idsa = row['id']
                        profil.PW = row['pass']
                        profil.telephone1 = row['telephone1'] if str(row['telephone1']).replace('.', '').replace(' ', '') != profil.telephone1 else profil.telephone1
                        profil.telephone2 = row['telephone2'] if str(row['telephone2']).replace('.', '').replace(' ', '') != profil.telephone2 else profil.telephone2
                        profil.voie1 =row['voie1']
                        profil.voie2 = row['voie2']
                        profil.voie3 = row['voie3']
                        profil.codepostal = row['codepostal']
                        profil.commune = row['commune']
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

                messages.success(request, str(total_created) + ' nouveaux utilisateur de cr??er')

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
                        inst, created = installation.objects.get_or_create(
                            idsa=row['id'])
                        # tc= row['type_communication'] if row['type_communication'] != np.nan else None

                        # inst.type_communication= tc,

                        inst.version_carte_firmware=row['version_carte_firmware'] if 'version_carte_firmware' in row and row['version_carte_firmware'] != np.nan else None,
                        inst.version_carte_interface=row['version_carte_interface'] if 'version_carte_interface' in row and row['version_carte_interface'] != np.nan else None,
                        inst.version_serveur_appli=row['version_serveur_appli'] if 'version_serveur_appli' in row and row['version_serveur_appli'] != np.nan else None,
                        inst.adresse_ip_wan=row['adresse_ip_wan'] if 'adresse_ip_wan' in row and row['adresse_ip_wan'] != np.nan else None,
                        inst.port_tcp_wan=row['port_tcp_wan'] if 'port_tcp_wan' in row and row['port_tcp_wan'] != np.nan else None
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
                        print(row)
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

                messages.success(request, str(total_created) + ' nouvelles donn??es')

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

class mail(View):
    login_url = '/login/'
    template_name = 'sav/mail.html'
    title = 'Ouvrir un ticket depuis la bo??te email sav'

    def dispatch(self, request, *args, **kwargs):
        return super(mail, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.emails = inbox.list(request)
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'emails': self.emails
                      }
                      )

    def post(self, request, *args, **kwargs):
        t_form = ticket_form(request.POST)
        e_form = add_evenement_form(request.POST, user=request.user,
                                        date=request.POST['mail_date'])
        json={}
        if e_form.is_valid():
            even=e_form.save(commit=False)
            json['evenement'] = {"form": "ok"}
        else:
            json['evenement'] = {"form": "nok", "error": e_form.errors}

        if t_form.is_valid():
            tick=t_form.save(commit=False)
            json['ticket'] = {"form": "ok"}
        else:
            json['ticket'] = {"form": "nok", "error": t_form.errors}

        if not e_form.is_valid() and t_form.is_valid():
            return JsonResponse(json, safe=False)
        else:
            even.save()
            tick.evenement=even
            tick.save()
        if request.POST['response']:
            date= datetime.strptime(request.POST['mail_date'], '%d-%m-%Y %H:%M')
            msg=inbox.mailbox_search(request, fetch=A(uid=request.POST['uid']
                                           ))
            if request.POST['response'] == 'send_response':
                try:
                    for m in msg:
                        subject = m.subject
                        if settings.DEBUG:
                            subject, from_email, to = m.subject, 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
                        else:
                            subject, from_email, to = m.subject, 'sav@solisart.fr', request.POST['response_email']

                        html_content = render_to_string('email/responsewithsignature.html', {
                            'oldmail': m.html,
                            'msg': request.POST['response_text']
                        })  # render with dynamic value
                        text_content = strip_tags(
                            html_content)  # Strip the html tag. So people can see the pure text at least.

                        # create the email, and attach the HTML version as well.
                        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                        msg.attach_alternative(html_content, "text/html")
                        msg.send()
                        json['email'] = {"send": "ok"}
                except Exception as e:

                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(e)
                    pass
                    json['email'] = {"send": "nok"}

            if request.POST['response'] == 'move_response':
                #todo when i have outlook 365
                    json['moveemail'] = {"todo": "ok"}

            if request.POST['response'] == 'login_response':
                try:
                    if settings.DEBUG:
                        subject, from_email, to = 'Identifiant pour my.solisart.fr', 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
                        utilisateur = User.objects.get(email='freddy.dubouchet@solisart.fr')
                    else:
                        subject, from_email, to = 'Identifiant pour my.solisart.fr', 'sav@solisart.fr', request.POST['response_email']
                        utilisateur=User.objects.get(email=request.POST['response_email'])

                    html_content = render_to_string('email/responseloselogin.html', {
                        'utilisateur':utilisateur,
                        'profil':profil_user.objects.get(user=utilisateur)
                    })  # render with dynamic value
                    text_content = strip_tags(
                        html_content)  # Strip the html tag. So people can see the pure text at least.

                    # create the email, and attach the HTML version as well.
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.mixed_subtype = 'related'
                    from django.templatetags.static import static
                    img_path=os.path.join(settings.STATIC_ROOT, 'image', 'login.png')
                    msg.mixed_subtype = 'related'
                    msg.attach_alternative(html_content, "text/html")
                    msg.attach(addimg(img_path, 'login'))
                    msg.send(fail_silently=False)

                    json['email'] = {"send": "ok"}
                except Exception as e:

                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(e)
                    pass
                    json['email'] = {"send": "nok"}

            if request.POST['response'] == 'reconnection':
                try:
                    if settings.DEBUG:
                        subject, from_email, to = 'Aide ?? la connexion du module SolisArt', 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
                    else:
                        subject, from_email, to = 'Aide ?? la connexion du module SolisArt', 'sav@solisart.fr', request.POST['response_email']

                    html_content = render_to_string('email/responsehelpconnection.html')  # render with dynamic value
                    text_content = strip_tags(
                        html_content)  # Strip the html tag. So people can see the pure text at least.

                    # create the email, and attach the HTML version as well.
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.mixed_subtype = 'related'
                    from django.templatetags.static import static
                    img_path=os.path.join(settings.STATIC_ROOT, 'image', 'aidereconnexion.jpg')
                    msg.mixed_subtype = 'related'
                    msg.attach_alternative(html_content, "text/html")
                    msg.attach(addimg(img_path, 'aidereconnexion'))
                    file_path=os.path.join(settings.STATIC_ROOT,'sav', 'fichier', 'procedure_connexion.pdf')
                    msg.attach_file(file_path)
                    msg.send(fail_silently=False)
                    json['email'] = {"send": "ok"}
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(e)
                    pass
                    json['email'] = {"send": "nok"}
        else:
            json['email'] = {"send": "pas demander"}

        return JsonResponse(json, safe=False)


class statistiques(View, SuccessMessageMixin):
    login_url = '/login/'
    template_name = 'sav/statistiques.html'
    title = 'Statistiques'

    def dispatch(self, request, *args, **kwargs):

        return super(statistiques, self).dispatch(request, *args, **kwargs)

    def titre_graph(self, frequence=None, periode=None):

        if frequence == "Rjour":
            titre = 'R??partition de hebdomadaire des tickets sur ' + periode + ' jours'
        elif frequence == "heure":
            titre = 'R??partition de journali??re des tickets sur ' + periode + ' jours'
        else:
            titre = 'R??partition des tickets par ' + str(frequence) + ' sur ' + periode + ' jours'
        return titre

    def chart_repartition_pb_cause_df(self, ponder=True, periode=None, P=None):
        from django.db.models import CharField
        try:
            if not periode:
                periode=30

            if P:
                queryset =self.filter_ticket(P)
            else:
                queryset = ticket.objects.filter(evenement__date__gte=datetime.today() - timedelta(days=int(periode))).order_by(
                'evenement__date')
            when = [When(probleme=v.id, then=Value(str(v))) for v in probleme.objects.all()]
            when2 = [When(cause=v.id, then=Value(str(v))) for v in cause.objects.all()]
            when3 = [When(evenement__installation__idsa__icontains=str(v), then=Value(v)) for v in range(2014, datetime.now().year+ 1, 1)]
            nb_install=installation.objects.all().count()
            from functools import reduce
            from operator import or_
            query= reduce(or_, (Q(idsa__icontains=t) for t in range(2015, datetime.now().year, 1)))
            ponde_before_2015= nb_install/installation.objects.exclude(query).count()
            when4 = [When(evenement__installation__idsa__icontains=str(v), then=nb_install/installation.objects.filter(idsa__icontains=str(v)).count()) for v in
                     range(2014, datetime.now().year + 1, 1)]
            queryset = queryset.annotate(
                annee=Case(*when3,default=Value("2000"), output_field=CharField())).values(
                'annee').annotate(
                ponder=Case(*when4,default=ponde_before_2015, output_field=FloatField())).values('annee',
                'ponder').order_by('probleme').annotate(
                pb=Case(*when, output_field=CharField())).values(
                'pb', 'annee','ponder').order_by('cause').annotate(
                cause=Case(*when2, output_field=CharField())).values(
                'cause', 'pb', 'annee', 'ponder')
            if ponder:
                queryset=queryset.annotate(count=Count('id')*F('ponder'))
            else:
                queryset = queryset.annotate(count=Count('id'))

            df = pd.DataFrame(list(queryset.order_by('annee', 'pb', 'cause').values('pb', 'cause','count', 'annee')))
            df.fillna(value="sans cause", inplace=True)
            return df
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            return None

    def chart_repartition_pb_cause(self, periode=None, ponder=True, P=None):
        from django.db.models import CharField
        try:
            df=self.chart_repartition_pb_cause_df(periode=periode, ponder=ponder, P=P)
            fig2 = px.sunburst({columns: list(df[columns]) for columns in df}, path=['annee','pb', 'cause'],
                               values='count', height=1000)
            fig2.update_traces(
                textinfo="label+value+percent parent + percent entry + text"
            )
            return fig2
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            return None

    def chart_repartition_temporel_df(self, frequence=None, periode=None, field=None, type=None):
        from django.db.models import CharField
        try:
            queryset = ticket.objects.filter(
                evenement__date__gte=datetime.today() - timedelta(days=int(periode))).order_by('evenement__date')

            if frequence == "semaine":
                queryset = queryset.annotate(frequence=TruncWeek('evenement__date'))
            if frequence == "mois":
                queryset = queryset.annotate(frequence=TruncMonth('evenement__date'))
            if frequence == "jour":
                queryset = queryset.annotate(frequence=TruncDay('evenement__date'))
            if frequence == "heure":
                queryset = queryset.annotate(frequence=ExtractHour('evenement__date'))
            if frequence == "Rjour":
                queryset = queryset.annotate(frequence=ExtractWeekDay('evenement__date'))

            if field == "forme":
                when = [When(forme=v.value, then=Value(v.name)) for v in forme_contact]
                queryset = queryset.order_by('frequence', 'forme').annotate(
                    lien=Case(*when, output_field=CharField())).values(
                    'frequence', 'lien').annotate(count=Count('id'))

            if field == "probleme":
                when = [When(probleme=v.id, then=Value(str(v))) for v in probleme.objects.all()]
                queryset = queryset.order_by('frequence', 'probleme').annotate(
                    lien=Case(*when, output_field=CharField())).values(
                    'frequence', 'lien').annotate(count=Count('id'))

            if field == "cause":
                when = [When(cause=v.id, then=Value(str(v))) for v in cause.objects.all()]
                queryset = queryset.order_by('frequence', 'cause').annotate(
                    lien=Case(*when, output_field=CharField())).values(
                    'frequence', 'lien').annotate(count=Count('id'))

            if field =="profil_type":
                when = [When(utilisateur__acces__profil_type=v.id, then=Value(str(v))) for v in profil_type.objects.all()]
                df = pd.DataFrame(columns=['frequence', 'lien'])
                for q in queryset:
                    try:
                        q.profil=str(profil_type.objects.get(acces__installation=q.evenement.installation, acces__utilisateur=q.utilisateur))
                    except:
                        q.profil="sans profil"
                    df = pd.concat([df, pd.Series({'frequence':str(q.frequence), 'lien':str(q.profil)}).to_frame().T], ignore_index=True)

                df = df.groupby(['frequence', 'lien'])['lien'].size().reset_index(name='count')

            if not 'df' in locals():
                df = pd.DataFrame(list(queryset.values('frequence', 'lien', 'count')))
            df.fillna(value="sans profil", inplace=True)

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            return None

        return df

    def chart_repartition_temporel(self, frequence=None, periode=None, field=None, type=None):
        try:
            df = self.chart_repartition_temporel_df(frequence=frequence, periode=periode, field=field, type=type)
            text_auto='s'
            if df.empty:
                return None
            else:
                if frequence == "Rjour":
                    semaine=['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
                    df['frequence']=pd.Series([semaine[i-2] for i in list(df['frequence'])])
                    titre='R??partition de hebdomadaire des tickets sur ' + periode + ' jours'
                    titlex="Jour de la semaine"
                elif frequence == "heure":
                    df=df.sort_values(by=['frequence'], ascending=True)
                    titre = 'R??partition de journali??re des tickets sur ' + periode + ' jours'
                    titlex="Heure ouverte de ticket"
                else:
                    df = df.sort_values(by='frequence')
                    titre='R??partition des tickets par ' + str(frequence) + ' sur ' + periode + ' jours'
                    titlex="Date"

                if type=="bar":
                    fig1 = px.bar(df,
                                  x='frequence',
                                  y='count',
                                  color='lien',
                                  text_auto=text_auto,
                                  title=titre
                                  )
                    fig1.update_xaxes(title=titlex)
                    fig1.update_yaxes(title='Nombre')
                    fig1.update_layout(height=600, legend=dict(title="L??gende"))
                    if frequence == 'heure':
                        fig1.update_layout(xaxis=dict(
                            tickvals=df['frequence'],
                            ticktext=[str(i) + ':00' for i in list(df['frequence'])]
                        ))
                    return fig1
                if type == "sunburst":
                    fig2 = px.sunburst({columns: list(df[columns]) for columns in df}, path=['frequence', 'lien'],
                                       values='count', height=600)

                    fig2.update_traces(
                        textinfo="label+value+percent parent + percent entry + text"
                    )
                    return fig2
        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            return None

    def filter_ticket(self, P):
        tickets = ticket.objects.filter(
            Q(cause__id__in=P.getlist('cause') if 'cause' in P else []) | \
            Q(cause=None if "0" in P.getlist('cause') else "0"),
            evenement__date__gte=datetime.strptime(P['date_start'], "%d-%m-%Y %H:%M"),
            evenement__date__lte=datetime.strptime(P['date_end'], "%d-%m-%Y %H:%M"),
            probleme__id__in=P.getlist('probleme') if 'probleme' in P else [])
        if 'annee' in P:
            conditions = Q(evenement__installation__idsa__icontains='xxxxxxxx')
            for tag in P.getlist('annee'):
                if tag == 'sans':
                    conditions |= ~Q(evenement__installation__idsa__icontains='20')
                else:
                    conditions |= Q(evenement__installation__idsa__icontains=tag)
            tickets = tickets.filter(conditions)

        if 'type' in P:
            conditions = Q(evenement__installation__idsa__icontains='xxxxxxxx')
            if 'sans' in P.getlist('type'):
                conditions |= ~Q(evenement__installation__idsa__icontains='20')
            if 'Z' in P.getlist('type'):
                conditions |= Q(evenement__installation__idsa__icontains="Z")
            if 'H' in P.getlist('type'):
                conditions |= Q(evenement__installation__idsa__icontains="HYDRO")
            if 'SC' in P.getlist('type'):
                conditions |= Q(evenement__installation__idsa__icontains="SC")

            tickets = tickets.filter(conditions)

        if 'detail' in P:
            conditions = Q(detail__icontains='xxxxxxxx')
            for tag in P['detail'].replace(' ', '').split(','):
                conditions |= Q(detail__icontains=tag)
            tickets = tickets.filter(conditions)

        if 'fichier' in P and P['fichier'] != '':
            conditions = Q(fichier__titre__icontains='xxxxxxxx')
            for tag in P['fichier'].replace(' ', '').split(','):
                conditions |= Q(fichier__titre__icontains=tag)
            tickets = tickets.filter(conditions)

        return tickets

    def get(self, request, *args, **kwargs):

        stattableauform=Stattableauform()

        try:
            fig1=self.chart_repartition_temporel(frequence="jour", periode="30", field="forme", type="bar")
            self.tickets_chart = opy.plot(fig1, output_type='div')
            fig2 = self.chart_repartition_temporel(frequence="jour", periode="30", field="forme", type="sunburst")
            self.sunburst = opy.plot(fig2, output_type='div')
            fig3 = self.chart_repartition_pb_cause(periode=30, ponder=True)
            self.sunburst2=""
            if fig3:
                self.sunburst2 = opy.plot(fig3, output_type='div')

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            messages.error(request, "Pas de donn??es avec ses crit??res")
            return render(request,
                          self.template_name,
                          {
                              'title': self.title,
                              'stattableauform':stattableauform
                          }
                          )
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'tickets_chart':self.tickets_chart,
                          'sunburst':self.sunburst,
                          'sunburst2': self.sunburst2,
                          'stattableauform':stattableauform
                      }
                      )

    def post(self, request, *args, **kwargs):

        if "download_csv2" in request.POST:

            df = self.chart_repartition_pb_cause_df(ponder='ponder' in request.POST, P=request.POST)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Statistiques Sympt??mes/causes.csv'
            df.to_csv(path_or_buf=response, index=False, encoding="utf-8")  # with other applicable parameters
            return response

        if "download_csv" in request.POST:
            df = self.chart_repartition_temporel_df(frequence=request.POST['frequence'],
                                                  periode=request.POST['periode'],
                                                  field=request.POST['field'])
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename='+self.titre_graph(frequence=request.POST['frequence'],
                                                  periode=request.POST['periode'])+'.csv'
            df.to_csv(path_or_buf=response)  # with other applicable parameters
            return response

        if "tableau" in request.POST:

            tickets = self.filter_ticket(request.POST)

            ticket_dict=[t.as_dict() for t in tickets]

            return render(request,
                      'widgets/table_stat.html',
                      {
                            'ticket':tickets,
                            'ticket_json': ticket_dict
                      }
                      )

        if "pbcause" in request.POST:
            fig = self.chart_repartition_pb_cause(ponder='ponder' in request.POST, P=request.POST)
            if fig:
                return HttpResponse(opy.plot(fig, output_type='div'))
            else:
                return HttpResponse('<div class="alert alert-danger" role="alert"><i class="fas fa-exclamation-triangle"></i>\
                          Pas de donn??e disponible avec ses crit??res de recherche\
                        </div>')

        if "field" in request.POST:
            fig = self.chart_repartition_temporel(frequence=request.POST['frequence'],
                                                  periode=request.POST['periode'],
                                                  field=request.POST['field'],
                                                  type=request.POST['type'])
            return HttpResponse(opy.plot(fig, output_type='div'))



class installation_view (View):
    login_url = '/login/'
    template_name = 'sav/installation.html'
    title = 'Installation'

    def dispatch(self, request, *args, **kwargs):

        self.pk = kwargs.pop('pk')
        self.instal = installation.objects.get(pk=self.pk)

        self.acces = acces.objects.filter(installation=self.instal).order_by('id').distinct()
        self.attribut_val = attribut_valeur.objects.filter(installation=self.instal)
        self.liste_evenements=evenement.objects.filter(installation=self.instal).order_by('-date')
        self.add_ticket_form = ticket_form(installation=self.instal)
        self.add_MES_form = MES_form(prefix="MES")
        self.add_evenement = add_evenement_form(user=request.user, installation=self.instal)
        self.add_problem = add_problem_form()
        self.form_class=installation_form(instance=self.instal)
        self.title = self.title + ' ' + str(self.instal)
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
                          'add_MES_form': self.add_MES_form,
                          'add_problem_form': self.add_problem,
                          'form': self.form_class,
                          'acces': self.acces
                      }
                      )

    def post(self, request, *args, **kwargs):

        if "alldownload" in request.POST:
            import zipfile
            tick = ticket.objects.get(pk=int(request.POST['ticket_id']))
            filenames = [ str(f.fichier.path) for f in tick.fichier.all()]
            # Folder name in ZIP archive which contains the above files
            # E.g [thearchive.zip]/somefiles/file2.txt
            zip_subdir = str(tick).replace("/", " ")
            zip_filename = "%s.zip" % zip_subdir

            # Open StringIO to grab in-memory ZIP contents
            s = BytesIO()

            # The zip compressor

            zf = zipfile.ZipFile(s, "w")

            for fpath in filenames:
                # Calculate path for file in zip
                fdir, fname = os.path.split(fpath)
                zip_path = os.path.join(zip_subdir, fname)

                # Add file, at correct path
                zf.write(fpath, zip_path)

            # Must close zip for all contents to be written
            zf.close()

            # Grab ZIP file from in-memory, make response with correct MIME-type
            resp = HttpResponse(s.getvalue(), content_type='application/zip')
            # ..and correct content-disposition
            resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
            return resp

        if "rotation" in request.POST:
            img=Fichiers.objects.get(pk=int(request.POST["id"]))
            original_photo = io.BytesIO(img.fichier.read())
            rotated_photo = io.BytesIO()

            image = Image.open(original_photo)
            image = image.rotate(int(request.POST["angle"]), expand=1)
            if img.extension().replace(".", '') == 'png':
                extention="PNG"
            else:
                extention="JPEG"
            image.save(rotated_photo, extention)
            img.fichier.save(img.fichier.name, ContentFile(rotated_photo.getvalue()))
            img.save()
            data={'rotation': 'ok'}
            return JsonResponse(data, safe=False)

        if "ticket_id" in request.POST or "MES_id" in request.POST:
            if "ticket_id" in request.POST:
                tic = ticket.objects.get(pk=int(request.POST["ticket_id"]))
            else:
                tic = MES.objects.get(pk=int(request.POST["MES_id"]))
            return render(request, "widgets/carouselImage.html",
                          {'tic': tic,
                           'photo_id': int(request.POST["photoid"])})

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

        elif "file_MES" in request.POST:
            form = FilesForm(request.POST, request.FILES)
            if form.is_valid():
                files = form.save()
                mes = MES.objects.get(pk=int(request.POST["file_MES"]))
                mes.fichier.add(files)
                data = {'is_valid': True, 'name': files.fichier.name, 'url': files.fichier.url, 'file_id': files.id,
                        'size': files.fichier.size}
            else:
                data = {'is_valid': False}
            return JsonResponse(data, safe=False)

        elif "GPS_id" in request.POST:
            a = attribut_valeur.objects.get(pk=request.POST['GPS_id'])
            a.valeur = request.POST['CoordonneeGPS']
            a.save()
            data={"valide": "ok", "message": "Modifer avec succ??s"}
            return JsonResponse(data, safe=False)

        elif "details" in request.POST:

            if "ta_ticket" in str(request.POST['id']):
                t= ticket.objects.get(pk=int(str(request.POST['id']).replace('ta_ticket_', '')))
                t.detail=request.POST['details']
                t.save()
                return JsonResponse({
                    "detail": "ok"
                }, safe=False)
            elif "ta_MES" in str(request.POST['id']):
                m= MES.objects.get(pk=int(str(request.POST['id']).replace('ta_MES_', '')))
                m.detail = request.POST['details']
                m.save()
                return JsonResponse({
                    "detail": "ok"
                }, safe=False)

        elif "submit" in request.POST:
            self.form_class=installation_form(request.POST, request.FILES, instance=self.instal)
            if self.form_class.is_valid():
                self.form_class.save()
                return HttpResponseRedirect(reverse('sav:installation', kwargs={'pk':int(self.instal.id)}))

        #n'est plus propos?? hidden
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
            else:
                return JsonResponse({
                    "ticket": "nok",
                    'error':self.add_evenement.errors
                }, safe=False)
            if self.add_ticket_form.is_valid():
                tick = self.add_ticket_form.save(commit=False)
                tick.evenement=even
                tick.detail=request.POST['detail']
                tick.save()
                return JsonResponse({
                    "ticket": "ok"
                }, safe=False)
            else:
                return JsonResponse({
                    "ticket": "nok",
                    'error':self.add_ticket_form.errors
                }, safe=False)

        elif request.POST['nature_form'] == "MES":

            self.add_evenement = add_evenement_form(request.POST,user=request.user, installation=self.instal)
            if self.add_evenement.is_valid():
                even = self.add_evenement.save()
                self.add_MES_form = MES_form(request.POST,prefix="MES")
            else:
                return JsonResponse({
                    "mes": "nok",
                    'error':self.add_evenement.errors
                }, safe=False)
            if self.add_MES_form.is_valid():
                tick = self.add_MES_form.save(commit=False)
                tick.evenement=even
                tick.save()
                return JsonResponse({
                    "mes": "ok"
                }, safe=False)
            else:
                return JsonResponse({
                    "ticket": "nok",
                    'error':self.add_ticket_form.errors
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
        if "ticket_commercial" in request.POST:
            tickets = self.profil.commercial_ticket(duree = int(request.POST['ticket_commercial']))
            return JsonResponse([t.as_dict() for t in tickets], safe=False)
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
    title = 'R??partition des installations'

    def dispatch(self, request, *args, **kwargs):

        return super(carte, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        data = profil_user.objects.filter(departement__isnull=False).order_by('user__first_name')
        dictionaries = [obj.as_dict() for obj in data]
        return render(request,
                      self.template_name,
                          {
                              'title': self.title,
                              'profils': json.dumps(dictionaries),
                              'install_total':attribut_valeur.objects.filter(attribut_def__description="Coordonn??es GPS DD") \
                                                .exclude(valeur="nan").count()
                          }
                      )

    def post(self, request, *args, **kwargs):

        if "adresse" in request.POST:
            import requests
            url = 'https://nominatim.openstreetmap.org/?q=' + request.POST['adresse'].replace(' ', '%') + '&format=json&polygon_geojson=1'
            return HttpResponse(requests.get(url), content_type='application/json; charset=utf-8')

        test = attribut_valeur.objects.filter(attribut_def__description="Coordonn??es GPS DD") \
            .exclude(valeur="nan")[int(request.POST['start']):int(request.POST['stop'])]
        from .templatetags.my_filter import Coor
        list_install=[]
        for t in test:
            popup='<b>Installation : </b><a href="/installation/'+ str(t.installation.id) +'">' + str(t.installation) + '</a>'
            if t.installation.proprio():
                popup+='<br><b>Propri??taire: </b><a href="/utilisateur/'+ str(t.installation.proprio().id) +'">'+ str(t.installation.proprio()) +'</a>'
            if t.installation.installateur():
                popup+='<br><b>Installateur: </b><a href="/utilisateur/'+ str(t.installation.installateur().id) +'">'+ str(t.installation.installateur()) +'</a>'
            list_install.append(
            {'type':'Feature',
             "properties": {
                 "name": str(t.installation),
                 "show_on_map": True if Coor(t.valeur) else False,
                 "popupContent": popup

             },
             "geometry": {
                 "type": "Point",
                 "coordinates": [float(i) for i in t.valeur.split(',')[::-1]] if Coor(t.valeur) else None
             }
             } )

        return HttpResponse(json.dumps(list_install), content_type="application/json")

class ticket_view(View):
    login_url = '/login/'
    template_name = 'sav/ticket.html'
    title = 'Tickets ouverts'

    def get(self, request, *args, **kwargs):
        from django.db.models import CharField, Value as V
        from django.db.models.functions import Concat
        all_ticket_open=ticket.objects.exclude(etat=3).order_by("-evenement__date").annotate(even_date=F('evenement__date'),
                                                                even_installation=F('evenement__installation'),
                                                                even_techncien_sav=F('evenement__technicien_sav'),
                                                                t_date=Func(F('evenement__date'),
                                                                            Value('DD-MM-YYYY HH:MM'),
                                                                            function='to_char',
                                                                            output_field=CharField()
                                                                            ))
        at=all_ticket_open.values()
        at2=[]
        for i in at:
            at2.append(i)
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'all_ticket_open':all_ticket_open,
                          'form_even':add_evenement_form(user=User.objects.get(pk=all_ticket_open[0].evenement.technicien_sav.id),
                                                         ),
                          'form_ticket':ticket_form,
                          'at_json': at2
                      }
        )

    def post(self, request, *args, **kwargs):
        form_evenement=add_evenement_form(request.POST, instance=evenement.objects.get(pk=request.POST['evenement']), user=User.objects.get(pk=int(request.POST['technicien_sav'])))
        form_ticket=ticket_form(request.POST, instance=ticket.objects.get(pk=request.POST['id']))
        data={}
        if form_evenement.is_valid():
            form_evenement.save()
            data['even'] = 'ok'
        else:
            data['even']=form_evenement.errors

        if form_ticket.is_valid():
            form_ticket.save()

            data['ticket']='ok'
        else:
            data['ticket'] = form_evenement.errors

        return JsonResponse(data, safe=False)


class bidouille (View):
    login_url = '/login/'
    template_name = 'sav/bidouille.html'
    title = 'Bidouille'

    def get(self, request, *args, **kwargs):

        from bs4 import BeautifulSoup
        import requests

        username = 'freddy.dubouchet@solisart.fr'
        password = 'uM(ij9ojEV'
        link = 'https://my.solisart.fr/'
        idsa = "GODIN"
        if True:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            driver = webdriver.Firefox(executable_path=r"C:\Users\freddy\Downloads\geckodriver-v0.32.0-win32\geckodriver.exe")
            driver.get(link)
            driver.find_element(By.ID, 'id').send_keys(username)
            driver.find_element(By.ID, 'pass').send_keys(password)
            driver.find_element(By.ID, 'connexion').click()
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

            driver.get('https://my.solisart.fr/admin/index.php?page=installation&id='+idsa)
            time.sleep(8)
            tt= driver.find_element(By.XPATH, '//label[@for="input-pages-visualisation"]')
            tt.click()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            time.sleep(8)
            src=soup.find('img', {'id':'schema-image'})['src']
            driver.get(
                'https://my.solisart.fr/admin/'+src)
            #Enregistrement du fichier ?? la racine
            driver.save_screenshot("schema.png")

            #Creation Fichiers
            file=Fichiers.objects.create(
                titre=idsa+'.png'
            )
            # driver.save_screenshot(idsa+'.png')
            namefile=idsa+'.png'

            image = Image.open("schema.png")
            # image = Image.open(namefile) #fonctionne avec un fichier exitant

            photo = io.BytesIO()
            image.save(photo, "png")
            #Sauvegarde de image
            file.fichier.save(namefile, ContentFile(photo.getvalue()))
            #supprimer le fichier ?? la racine
            os.remove("schema.png")
            #Fermer le navigateur firefox
            driver.close()

        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )

