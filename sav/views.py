# -*- coding: utf-8 -*-
import datetime
import glob
import io
import json
import os
import sys
import time
from datetime import timedelta
from email.mime.image import MIMEImage
from io import StringIO
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files import File
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, Count, F, When, Value, Case, CharField, Func, Subquery, FloatField, IntegerField, OuterRef, TextField
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncHour, ExtractHour, ExtractDay, \
    ExtractWeekDay, Cast, ExtractIsoWeekDay
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from django.views import View
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from plotly.subplots import make_subplots

from heraklesinfo.models import C100Clients
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
    def mailbox():
        email_user = "sav@solisart.fr"
        email_pass = "AristideBerges218"
        server = 'imap.webmo.fr'

        return MailBox(server).login(email_user, email_pass)

    def mailbox_search(fetch=None, days=None):
        if not days:
            days = 3
        if not fetch:
            fetch = A(date_gte=(datetime.now() - timedelta(days=days)).date())
        else:
            fetch = A(fetch, date_gte=(datetime.now() - timedelta(days=days)).date())

        return inbox.mailbox().fetch(fetch)

    def fileattchment(msg):
        return [{'name':att.filename, 'type':att.content_type} for att in msg.attachments]
        # for att in msg.attachments:
        #     print(att.filename, att.content_type)
        #     with open('C:/1/{}'.format(att.filename), 'wb') as f:
        #         f.write(att.payload)

    def list(request, fetch=None):

        mailbox = inbox.mailbox_search(fetch=None, days=3)
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
        from django_celery_results.models import TaskResult
        from django.db.models import Max
        Tasks = TaskResult.objects.filter(pk__in=TaskResult.objects.all().order_by("task_name").values('task_name').annotate(Max('id')).values_list('id__max', flat=True))
        return render(request,
                      self.template_name,
                      {
                          'title':self.title,
                          'form': self.form_class,
                          'tasks':Tasks
                      }
                      )

    def post(self, request, *args, **kwargs):

        if 'exportprix' in request.POST:
            from .tasks import actualisePrixMySolisart
            return actualisePrixMySolisart()

        if 'submit' in request.POST:
            uploaded_file = request.FILES['fichier']
            df = pd.read_csv(uploaded_file, on_bad_lines='skip', header=None)
            dictionary = {
                'Ã©': 'é',
                'Ã¨': 'è',
                'Ã«':'ë',
                'Ã§':'ç',
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
                from .tasks import ActualiseUtilisateur
                ActualiseUtilisateur.apply_async(kwargs={'df_as_dict':df.to_dict()})

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
                from .tasks import ActualiseInstallation
                ActualiseInstallation.apply_async(kwargs={'df_as_dict':df.to_dict()})

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
                from .tasks import ActualiseAttribut
                ActualiseAttribut.apply_async(kwargs={'df_as_dict':df.to_dict()})

            if 'acces' in uploaded_file.name:
                from .tasks import ActualiseAcces
                ActualiseAcces.apply_async(kwargs={'df_as_dict':df.to_dict()})

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
                from .tasks import ActualiseHistorique
                ActualiseHistorique.apply_async(kwargs={'df_as_dict':df.to_dict()})

        return render(request,
                      self.template_name,
                      {
                          'title':self.title,
                          'form': self.form_class
                      }
                      )

# class mail(View):
#     login_url = '/login/'
#     template_name = 'sav/mail.html'
#     title = 'Ouvrir un ticket depuis la boîte email sav'
#
#     def dispatch(self, request, *args, **kwargs):
#         return super(mail, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         self.emails = emailbox.objects.all()
#
#         return render(request,
#                       self.template_name,
#                       {
#                           'title': self.title,
#                           'emails': self.emails
#                       }
#                       )
#
#     def post(self, request, *args, **kwargs):
#
#
#         print(request.POST)
#         if 'createticket' in request.POST:
#             msg = emailbox.objects.get(pk=request.POST['id'])
#             return render(request, 'widgets/ticketSinceEmail.html',
#                           {
#                               'e':msg,
#                               'add_evenement_form': add_evenement_form(user=request.user, user_acces=msg.from_user)
#                           })
#
#
#         t_form = ticket_form(request.POST)
#         e_form = add_evenement_form(request.POST, user=request.user,
#                                         date=request.POST['mail_date'])
#         json={}
#         if e_form.is_valid():
#             even=e_form.save(commit=False)
#             json['evenement'] = {"form": "ok"}
#         else:
#             json['evenement'] = {"form": "nok", "error": e_form.errors}
#
#         if t_form.is_valid():
#             tick=t_form.save(commit=False)
#             json['ticket'] = {"form": "ok"}
#         else:
#             json['ticket'] = {"form": "nok", "error": t_form.errors}
#
#         if not e_form.is_valid() and t_form.is_valid():
#             return JsonResponse(json, safe=False)
#         else:
#             e = even.save()
#             tick.evenement=e
#             tick.save()
#         if request.POST['response']:
#             date= datetime.strptime(request.POST['mail_date'], '%d-%m-%Y %H:%M')
#             msg=emailbox.objects.filter(pk=request.POST['mail_id'])
#             if request.POST['response'] == 'send_response':
#                 try:
#                     for m in msg:
#                         if settings.DEBUG:
#                             subject, from_email, to = m.subject, 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
#                         else:
#                             subject, from_email, to = m.subject, 'sav@solisart.fr', request.POST['response_email']
#
#                         html_content = render_to_string('email/responsewithsignature.html', {
#                             'oldmail': m.html,
#                             'msg': request.POST['response_text']
#                         })  # render with dynamic value
#                         text_content = strip_tags(
#                             html_content)  # Strip the html tag. So people can see the pure text at least.
#
#                         # create the email, and attach the HTML version as well.
#                         msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                         msg.attach_alternative(html_content, "text/html")
#                         msg.send()
#                         json['email'] = {"send": "ok"}
#                 except Exception as e:
#
#                     exc_type, exc_obj, exc_tb = sys.exc_info()
#                     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                     print(exc_type, fname, exc_tb.tb_lineno)
#                     print(e)
#                     pass
#                     json['email'] = {"send": "nok"}
#
#             if request.POST['response'] == 'move_response':
#                 #todo when i have outlook 365
#                     json['moveemail'] = {"todo": "ok"}
#
#             if request.POST['response'] == 'login_response':
#                 try:
#                     if settings.DEBUG:
#                         subject, from_email, to = 'Identifiant pour my.solisart.fr', 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
#                         utilisateur = User.objects.filter(email='freddy.dubouchet@solisart.fr')[0]
#                     else:
#                         subject, from_email, to = 'Identifiant pour my.solisart.fr', 'sav@solisart.fr', request.POST['response_email']
#                         utilisateur=User.objects.filter(email=request.POST['response_email'])[0]
#
#                     html_content = render_to_string('email/responseloselogin.html', {
#                         'utilisateur':utilisateur,
#                         'profil':profil_user.objects.get(user=utilisateur)
#                     })  # render with dynamic value
#                     text_content = strip_tags(
#                         html_content)  # Strip the html tag. So people can see the pure text at least.
#
#                     # create the email, and attach the HTML version as well.
#                     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.mixed_subtype = 'related'
#                     from django.templatetags.static import static
#                     img_path=os.path.join(settings.STATIC_ROOT, 'image', 'login.png')
#                     msg.mixed_subtype = 'related'
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.attach(addimg(img_path, 'login'))
#                     msg.send(fail_silently=False)
#
#                     json['email'] = {"send": "ok"}
#                 except Exception as e:
#
#                     exc_type, exc_obj, exc_tb = sys.exc_info()
#                     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                     print(exc_type, fname, exc_tb.tb_lineno)
#                     print(e)
#                     pass
#                     json['email'] = {"send": "nok"}
#
#             if request.POST['response'] == 'reconnection':
#                 try:
#                     if settings.DEBUG:
#                         subject, from_email, to = 'Aide à la connexion du module SolisArt', 'sav@solisart.fr', 'freddy.dubouchet@solisart.fr'
#                     else:
#                         subject, from_email, to = 'Aide à la connexion du module SolisArt', 'sav@solisart.fr', request.POST['response_email']
#
#                     html_content = render_to_string('email/responsehelpconnection.html')  # render with dynamic value
#                     text_content = strip_tags(
#                         html_content)  # Strip the html tag. So people can see the pure text at least.
#
#                     # create the email, and attach the HTML version as well.
#                     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.mixed_subtype = 'related'
#                     from django.templatetags.static import static
#                     img_path=os.path.join(settings.STATIC_ROOT, 'image', 'aidereconnexion.jpg')
#                     msg.mixed_subtype = 'related'
#                     msg.attach_alternative(html_content, "text/html")
#                     msg.attach(addimg(img_path, 'aidereconnexion'))
#                     file_path=os.path.join(settings.STATIC_ROOT,'sav', 'fichier', 'procedure_connexion.pdf')
#                     msg.attach_file(file_path)
#                     msg.send(fail_silently=False)
#                     json['email'] = {"send": "ok"}
#                 except Exception as e:
#                     exc_type, exc_obj, exc_tb = sys.exc_info()
#                     fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#                     print(exc_type, fname, exc_tb.tb_lineno)
#                     print(e)
#                     pass
#                     json['email'] = {"send": "nok"}
#         else:
#             json['email'] = {"send": "pas demander"}
#
#         return JsonResponse(json, safe=False)

class statistiques(View, SuccessMessageMixin):
    login_url = '/login/'
    template_name = 'sav/statistiques.html'
    title = 'Statistiques'

    def dispatch(self, request, *args, **kwargs):

        return super(statistiques, self).dispatch(request, *args, **kwargs)

    def titre_graph(self, frequence=None, periode=None):

        if frequence == "Rjour":
            titre = 'Répartition de hebdomadaire des tickets sur ' + periode + ' jours'
        elif frequence == "heure":
            titre = 'Répartition de journalière des tickets sur ' + periode + ' jours'
        else:
            titre = 'Répartition des tickets par ' + str(frequence) + ' sur ' + periode + ' jours'
        return titre

    def chart_repartition_pb_cause_df(self, periode=None, P=None):
        from django.db.models import CharField
        from django.db.models import OuterRef, Subquery, Count

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

            if P and P["repartition"] == 'acces':
                queryset = queryset.annotate(
                    installation_id=F('evenement__installation')
                ).values("installation_id", "utilisateur").annotate(profil_type_id=Subquery(
                    acces.objects.filter(installation__id=OuterRef("installation_id"),
                                         utilisateur__id=OuterRef("utilisateur")).values('profil_type')[:1]))
                when4 = [When(profil_type_id=v.id, then=Value(str(v))) for v in
                         profil_type.objects.all()]
                queryset = queryset.order_by('profil_type_id').annotate(
                    annee=Case(*when4, output_field=CharField())
                ).values('annee')
                queryset=queryset.annotate(
                    pb=Case(*when, output_field=CharField())).values(
                    'pb', 'annee').order_by('cause').annotate(
                    cause=Case(*when2, output_field=CharField())).values(
                    'cause', 'pb', 'annee')
                queryset = queryset.annotate(count=Count('id'))
                df = pd.DataFrame(
                    list(queryset.order_by('annee', 'pb', 'cause').values('pb', 'cause', 'count', 'annee')))
                df.fillna(value="sans cause", inplace=True)
                return df
            else:
                nb_install=installation.objects.all().count()
                from functools import reduce
                from operator import or_
                query= reduce(or_, (Q(idsa__icontains=t) for t in range(2015, datetime.now().year, 1)))
                ponde_before_2015= nb_install/installation.objects.exclude(query).count()
                when5 = [When(evenement__installation__idsa__icontains=str(v), then=nb_install/installation.objects.filter(idsa__icontains=str(v)).count()) for v in
                         range(2014, datetime.now().year + 1, 1)]

                queryset = queryset.annotate(
                    annee=Case(*when3,default=Value("2000"), output_field=CharField())).values(
                    'annee').annotate(
                    ponder=Case(*when5,default=ponde_before_2015, output_field=FloatField())).values('annee',
                    'ponder').order_by('probleme').annotate(
                    pb=Case(*when, output_field=CharField())).values(
                    'pb', 'annee','ponder').order_by('cause').annotate(
                    cause=Case(*when2, output_field=CharField())).values(
                    'cause', 'pb', 'annee', 'ponder')

            if P and P["repartition"] == "annuelP":
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

    def chart_repartition_pb_cause(self, periode=None, P=None):
        from django.db.models import CharField
        try:
            df=self.chart_repartition_pb_cause_df(periode=periode, P=P)
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
            from django.utils import timezone
            queryset = ticket.objects.filter(
                evenement__date__gte=timezone.now() - timedelta(days=int(periode))).order_by('evenement__date')

            if frequence == "semaine":
                queryset = queryset.annotate(freq=TruncWeek('evenement__date'))
                format_str='sWW - yyyy.MM.dd'
                queryset = queryset.annotate(
                    frequence=Func(
                        F('freq'),
                        Value(format_str),
                        function='to_char',
                        output_field=CharField()
                    )
                )

            if frequence == "mois":
                queryset = queryset.annotate(freq=TruncMonth('evenement__date'))
                format_str = 'YYYY-MM'
                queryset = queryset.annotate(
                    frequence=Func(
                        F('freq'),
                        Value(format_str),
                        function='to_char',
                        output_field=CharField()
                    )
                )

            if frequence == "jour":
                queryset = queryset.annotate(freq=TruncDay('evenement__date'))
                format_str = 'yyyy-MM-dd'
                queryset = queryset.annotate(
                    frequence=Func(
                        F('freq'),
                        Value(format_str),
                        function='to_char',
                        output_field=CharField()
                    )
                )

            if frequence == "heure":
                import zoneinfo
                paris = zoneinfo.ZoneInfo('Europe/Paris')
                with timezone.override(paris):
                    queryset = queryset.annotate(frequence=ExtractHour('evenement__date'))
            if frequence == "Rjour":
                import zoneinfo
                paris = zoneinfo.ZoneInfo('Europe/Paris')
                with timezone.override(paris):
                    queryset = queryset.annotate(frequence=ExtractIsoWeekDay('evenement__date'))

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
                queryset = queryset.order_by('freq', 'cause').annotate(
                    lien=Case(*when, output_field=CharField())).values(
                    'frequence', 'lien').annotate(count=Count('id'))

            if field =="profil_type":
                queryset = queryset.order_by('freq').annotate(
                    installation_id=F('evenement__installation')
                ).values("installation_id", "utilisateur", "frequence").annotate(profil_type_id=Subquery(
                    acces.objects.filter(installation__id=OuterRef("installation_id"),
                                         utilisateur__id=OuterRef("utilisateur")).values('profil_type')[:1]))

                when4 = [When(profil_type_id=v.id, then=Value(str(v))) for v in
                         profil_type.objects.all()]

                queryset = queryset.order_by('frequence','profil_type_id').annotate(
                    lien=Case(*when4, output_field=CharField())
                )
                queryset= queryset.values('frequence', 'lien').order_by("frequence", "lien").annotate(count=Count('id'))
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
                    df['frequence']=pd.Series([semaine[i-1] for i in list(df['frequence'])])
                    titre='Répartition de hebdomadaire des tickets sur ' + periode + ' jours'
                    titlex="Jour de la semaine"
                elif frequence == "heure":
                    df=df.sort_values(by=['frequence'], ascending=True)
                    titre = 'Répartition de journalière des tickets sur ' + periode + ' jours'
                    titlex="Heure ouverte de ticket"
                else:
                    df = df.sort_values(by='frequence')
                    titre='Répartition des tickets par ' + str(frequence) + ' sur ' + periode + ' jours'
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
                    fig1.update_layout(height=600, legend=dict(title="Légende"))
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
        if 'article_BL' in P:
            conditions = Q(codouv__exact='xxxxxxxx')
            for article in P.getlist('article_BL'):
                conditions |= Q(codouv__exact = article)

            BLs = C701Ouvraof.objects.db_manager('herakles'). \
                filter(conditions). \
                order_by("codeof"). \
                values_list("codeof", flat=True)
            condition2 = Q(BL__BL__in = list(BLs))
            if "sans" in P.getlist('article_BL'):
                condition2 |= Q(BL__isnull=True)
            tickets = tickets.filter(condition2)

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
        start = timezone.now()-timedelta(days =30)
        BLwithticket = ticket.objects.filter(
            BL__isnull=False,
            evenement__date__gte=start,
            evenement__date__lte=timezone.now(),
        ).values_list('BL__BL', flat=True)
        from django.db.models import Sum
        ArticlesBl = C701Ouvraof.objects.db_manager('herakles').\
                    filter(codeof__in= list(BLwithticket)).\
                    exclude(codouv="TEXTE").\
                    annotate(
                        qte= Cast("nbre", output_field=(FloatField())),
                        prixunitaire = Cast("pvbase", output_field=(FloatField())),
                        remisepct = Cast("rem", output_field=(FloatField()))
                    ).\
                    order_by("codouv", 'remisepct'). \
                    values("codouv", "remisepct", "qte", "prixunitaire").\
                    annotate(
                        qtet=Sum("qte"),
                        remise=F("prixunitaire") * F("qtet") * F('remisepct') * 0.01,
                        total=F("prixunitaire") * F("qtet"),
                        totalremise=F("total") - F("remise")
                    ).\
                    values("codouv", "titre", "qtet", "prixunitaire","remisepct", 'total','totalremise')
        ArticlesBl =list(ArticlesBl)

        try:
            fig1=self.chart_repartition_temporel(frequence="semaine", periode="120", field="forme", type="bar")
            self.tickets_chart = opy.plot(fig1, output_type='div')
            fig2 = self.chart_repartition_temporel(frequence="semaine", periode="120", field="forme", type="sunburst")
            self.sunburst = opy.plot(fig2, output_type='div')
            fig3 = self.chart_repartition_pb_cause()
            self.sunburst2=""
            if fig3:
                self.sunburst2 = opy.plot(fig3, output_type='div')

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(ex)
            messages.error(request, "Pas de données avec ses critères")
            return render(request,
                          self.template_name,
                          {
                              'title': self.title,
                              'stattableauform':stattableauform,
                              'ArticlesBl':  ArticlesBl
                          }
                          )
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'tickets_chart':self.tickets_chart,
                          'sunburst':self.sunburst,
                          'sunburst2': self.sunburst2,
                          'stattableauform':stattableauform,
                          'ArticlesBl':  ArticlesBl
                      }
                      )

    def post(self, request, *args, **kwargs):

        if "refreshBL" in request.POST:
            start = datetime.strptime(request.POST['date_start_BL'], "%d-%m-%Y %H:%M")
            end = datetime.strptime(request.POST['date_end_BL'], "%d-%m-%Y %H:%M")
            BLwithticket = ticket.objects.filter(
                BL__isnull=False,
                evenement__date__gte=start,
                evenement__date__lte=end,
            ).values_list('BL__BL', flat=True)
            from django.db.models import Sum
            ArticlesBl = C701Ouvraof.objects.db_manager('herakles'). \
                exclude(codouv='TEXTE').\
                filter(codeof__in=list(BLwithticket)). \
                annotate(
                qte=Cast("nbre", output_field=(FloatField())),
                prixunitaire=Cast("pvbase", output_field=(FloatField())),
                remisepct=Cast("rem", output_field=(FloatField()))
            ). \
                order_by("codouv", 'remisepct'). \
                values("codouv", "remisepct", "qte", "prixunitaire"). \
                annotate(
                qtet=Sum("qte"),
                remise=F("prixunitaire") * F("qtet") * F('remisepct') * 0.01,
                total=F("prixunitaire") * F("qtet"),
                totalremise=F("total") - F("remise")
            ). \
                values("codouv", "titre", "qtet", "prixunitaire", "remisepct", 'total', 'totalremise')
            ArticlesBl = list(ArticlesBl)
            return JsonResponse(ArticlesBl, safe=False)

        if "download_csv2" in request.POST:

            df = self.chart_repartition_pb_cause_df(P=request.POST)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=Statistiques Symptômes/causes.csv'
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
            fig = self.chart_repartition_pb_cause(P=request.POST)
            if fig:
                return HttpResponse(opy.plot(fig, output_type='div'))
            else:
                return HttpResponse('<div class="alert alert-danger" role="alert"><i class="fas fa-exclamation-triangle"></i>\
                          Pas de donnée disponible avec ses critères de recherche\
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

        print(request.POST)

        if "dynamicsolution" in request.POST:
            if request.POST["dynamicsolution"]:
                solutions = cause.objects.get(pk=request.POST["dynamicsolution"]).solution.all()
                if solutions:
                    html='<h3>Solutions associées:</h3><ul>'
                    for s in solutions:
                        html+='<li>'+ str(s) + '</li>'
                    html+='</ul>'
                else:
                    html = ''
            else:
                html=''
            return HttpResponse(html)

        if "dynamiccauces" in request.POST:
            causes = probleme.objects.get(pk=request.POST["dynamiccauces"]).causes.all()
            if not causes:
                causes = cause.objects.all()
            html='<option value="" selected="">---------</option>'
            categorie=''
            i = 0
            for c in causes:
                if c.categorie != categorie and i != 0:
                    html += '</optgroup>'
                if c.categorie != categorie:
                    html+="<optgroup label='" + str(type_cause(c.categorie).label) +"'>"
                    categorie = c.categorie
                html+= "<option value='" + str(c.id) + "'>" + str(c.sous_categorie)+"</option>"
                i+=1
            html+='</optgroup>'

            return HttpResponse(html)

        if "BL_popover" in request.POST:
            from heraklesinfo.models import C701Ouvraof
            articles = C701Ouvraof.objects.db_manager('herakles').\
                filter(codeof__icontains=request.POST["BL_popover"].replace(' ', '')).\
                annotate(qte= Cast("nbre", output_field=(FloatField()))).\
                values("codouv", "qte", "titre")

            return render(request,"widgets/tableauBL_articles.html",
                          {'articles': articles})

        if "devis_popover" in request.POST:
            from heraklesinfo.models import C105LignesDeDevis
            articles = C105LignesDeDevis.objects.db_manager('herakles').\
                filter(t105_1_code_devis__icontains=request.POST["devis_popover"].replace(' ', '')).\
                annotate(
                    codouv = F('t105_6_code_composant'),
                    qte= Cast("t105_34_qté_vendue", output_field=(FloatField())),
                    titre = F('t105_40_titre_de_ligne')
            ).\
                values("codouv", "qte", "titre")

            return render(request,"widgets/tableauBL_articles.html",
                          {'articles': articles})

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
            data={"valide": "ok", "message": "Modifer avec succès"}
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

        #n'est plus proposé hidden
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
                if 'BL' in request.POST:
                    for b in request.POST.getlist('BL'):
                        tick.BL.add(BL_herakles.objects.get(pk=b))
                if 'devis' in request.POST:
                    for d in request.POST.getlist('devis'):
                        tick.devis.add(devis_herakles.objects.get(pk=d))
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

        if 'herakles' in request.POST:
            if self.profil.Client_herakles:
                client = C100Clients.objects.db_manager('herakles').get(t100_1_code_client__exact=self.profil.Client_herakles)
                return render(request, "widgets/client_herakles.html",
                              {'client': {str(key).replace('t100_', '').replace('_', ' '): value for key, value in client.__dict__.items() }})
            else:
                return HttpResponse("<h2 class='text-danger'>Client Hérakles non renseigné</h2>")
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
    title = 'Répartition des installations'

    def dispatch(self, request, *args, **kwargs):

        return super(carte, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        #tous les utilisateurs ayant des départements sauf samuel Ronsin
        data = profil_user.objects.filter(departement__isnull=False).exclude(user_id=6846).order_by('user__first_name')
        dictionaries = [obj.as_dict() for obj in data]
        return render(request,
                      self.template_name,
                          {
                              'title': self.title,
                              'profils': json.dumps(dictionaries),
                              'install_total':attribut_valeur.objects.filter(attribut_def__description="Coordonnées GPS DD") \
                                                .exclude(valeur="nan").count()
                          }
                      )

    def post(self, request, *args, **kwargs):

        if "adresse" in request.POST:
            import requests
            url = 'https://nominatim.openstreetmap.org/?q=' + request.POST['adresse'].replace(' ', '%') + '&format=json&polygon_geojson=1'
            return HttpResponse(requests.get(url), content_type='application/json; charset=utf-8')

        test = attribut_valeur.objects.filter(attribut_def__description="Coordonnées GPS DD") \
            .exclude(valeur="nan")[int(request.POST['start']):int(request.POST['stop'])]
        from .templatetags.my_filter import Coor
        list_install=[]
        for t in test:
            popup='<b>Installation : </b><a href="/installation/'+ str(t.installation.id) +'">' + str(t.installation) + '</a>'
            if t.installation.proprio():
                popup+='<br><b>Propriétaire: </b><a href="/utilisateur/'+ str(t.installation.proprio().id) +'">'+ str(t.installation.proprio()) +'</a>'
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

        t = datetime.now()
        from django.db.models import CharField
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
        form_even = add_evenement_form(user=User.objects.get(pk=all_ticket_open[0].evenement.technicien_sav.id))
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'all_ticket_open':all_ticket_open,
                          'form_even':form_even,
                          'form_ticket':ticket_form,
                          'at_json': at2
                      }
        )

    def post(self, request, *args, **kwargs):

        if "nature_form" in request.POST:
            add_ticket_form = ticket_form(instance=ticket.objects.get(pk=int(request.POST['id'])), installation=ticket.objects.get(pk=int(request.POST['id'])).evenement.installation)
            add_evenement = add_evenement_form(
                instance=evenement.objects.get(ticket__pk=int(request.POST['id'])),
                user=ticket.objects.get(pk=int(request.POST['id'])).evenement.technicien_sav,
                installation=ticket.objects.get(pk=int(request.POST['id'])).evenement.installation)

            return render(request, "widgets/crispy_form.html",
                      {'add_ticket_form': add_ticket_form,
                       'add_evenement': add_evenement})
        else:
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

            if data['even']=='ok' and data['ticket']=='ok':
                data['ticketChanged']=ticket.objects.filter(pk=request.POST['id']).order_by("-evenement__date").annotate(even_date=F('evenement__date'),
                                                                                     even_installation=F(
                                                                                         'evenement__installation'),
                                                                                     even_techncien_sav=F(
                                                                                         'evenement__technicien_sav')).values()[0]

            return JsonResponse(data, safe=False)


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def send_channel_message(group_name, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        '{}'.format(group_name),
        {
            'type': 'channel_message',
            'message': message
        }
    )


class bidouille (View):
    login_url = '/login/'
    template_name = 'sav/bidouille.html'
    title = 'Bidouille'

    def get(self, request, *args, **kwargs):

        send_channel_message('cartcreating', 'well done')



        # from .tasks import actualisePrixMySolisart, actualise_herakles, actualise_client_herakles, cleanTaskResult
        # cleanTaskResult()
        # actualisePrixMySolisart()
        # actualise_herakles.delay()
        # from django.db.models import CharField
        # from django.db.models.functions import Length
        # TextField.register_lookup(Length, 'length')
        # instal = installation.objects.filter(
        #     attribut_valeur__attribut_def__description="Code postal"
        # ).annotate(
        #     num_departement1=Subquery(
        #     attribut_valeur.objects.filter(installation__pk=OuterRef("id"), attribut_def__description="Code postal").values('valeur')[:1]
        #     ),
        #     num_departement2 = Substr('num_departement1', 1, 2),
        #     num_departement=Case(
        #         When(num_departement1__length=4, then=Value(str(100))),
        #         When(num_departement1__length=5, then='num_departement2'),
        #         output_field=CharField())
        # ).filter(num_departement__in=list(['100']))
        # for i in instal:
        #     print(i, i.num_departement)
        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )


class bibliotheque(View):
    login_url = '/login/'
    template_name = 'sav/bibliotheque.html'
    title = 'Bibliothèque documentaire'
    form = ajouter_procedure_form()

    def get(self, request, *args, **kwargs):
        self.c = classification.objects.all().order_by("dossier", "titre")
        if  'pk' in kwargs:
            self.pk = kwargs.pop('pk')
        else:
            self.pk=None
        return render(request,
                      self.template_name,
                      {
                          'title': self.title,
                          'classification': self.c,
                          'form':self.form,
                          'classification_form': classification_form(),
                          'pk':self.pk
                      }
                      )

    def post(self, request, *args, **kwargs):
        from .models import classification
        self.c = classification.objects.all().order_by("dossier", "titre")
        #Permet  d'enregister les nouvelles procédures
        if "nouvelle_procedure" in request.POST:
            class_form=classification_form(request.POST)
            if class_form.is_valid():
                if request.POST['titre'] == str('0'):
                    classif = class_form.save()
                    classif.titre = request.POST['autre']
                    classif.save()
                else:
                    classif=classification.objects.get(pk=request.POST['titre'])
                form2 = ajouter_procedure_form(request.POST, request.FILES)
                if form2.is_valid():
                    form2.save(commit=False)
                    doc = form2.save()
                    doc.classification = classif
                    doc.save()
                    return HttpResponseRedirect(reverse('sav:bibliotheque'))
                else:
                    return render(request,
                           self.template_name,
                           {
                               'title': self.title,
                               'form': form2,
                               'classification_form': class_form
                           }
                           )
            else:
                return render(request,
                       self.template_name,
                       {
                           'title': self.title,
                           'classification': self.c,
                           'form': self.form(request.POST),
                           'classification_form': classification_form(request.POST)
                       }
                       )

        #Charger tous l'historique avec duagramme de gantt et tableau de tous les versions
        if "charger" in request.POST:
            from django.db.models.functions import StrIndex
            fichiers = documentation.objects.filter(classification__id=request.POST['charger']).\
                annotate(split=StrIndex(F('fichier'), V('.')))\
                .annotate(extension=Substr(F('fichier'), F('split')+1))\
                .order_by('extension','date')
            list=[]
            extension=''
            for f in fichiers:
                if f != fichiers[0] and extension == f.extension:
                    dictionary = dict(Extention=extension, Start=start, Finish=f.date.strftime('%Y-%m-%d'), Version=version + ' ' + extension)
                    list.append(dictionary)
                    start = f.date.strftime('%Y-%m-%d')
                    version=f.version
                elif f != fichiers[0] and extension != f.extension:
                    dictionary = dict(Extention=extension, Start=start, Finish=datetime.today().strftime('%Y-%m-%d'), Version=version + ' ' + extension)
                    list.append(dictionary)
                    start = f.date.strftime('%Y-%m-%d')
                    version=f.version
                    extension = f.extension
                else:
                    start = f.date.strftime('%Y-%m-%d')
                    version=f.version
                    extension=f.extension
                if f == fichiers.reverse()[0]:
                    finish = datetime.today().strftime('%Y-%m-%d')
                    dictionary = dict(Extention=extension, Start=start, Finish=finish, Version=f.version  + ' ' + extension)
                    list.append(dictionary)
            fig = px.timeline(pd.DataFrame(list),
                              x_start="Start",
                              x_end="Finish",
                              y="Version",
                              color="Extention",
                              title='Chronologie pour ' + str(fichiers[0].classification)
                              )
            return render(request,
                       'widgets/table_documentation.html',
                       {
                           'fichiers': fichiers,
                           'graph':opy.plot(fig, output_type='div')
                       }
                       )

        #Rend dynamique le form de création de procédure
        if "refresh" in request.POST:
            from .models import classification
            if 'categorie' in request.POST:
                docs = classification.objects.filter(
                categorie=request.POST['categorie'],
                dossier=request.POST['dossier'],
                sous_dossier = request.POST['sous_dossier']
            )
            else:
                docs = classification.objects.filter(
                    categorie=request.POST['update-categorie'],
                    dossier=request.POST['update-dossier'],
                    sous_dossier=request.POST['update-sous_dossier']
                )
            html=''
            for doc in docs:
                html+='<option value='+str(doc.id)+'>' + str(doc.titre) + '</option>'
            html+='<option value="0">Autre</option>'
            return HttpResponse(html)

        #Message de confirmation de suppression ou page de modification
        if "Confirm" in request.POST:
            id_input = '<input type=hidden name="id" value=' + request.POST['id'] + '>'
            if request.POST['mode']== 'Supprimer':
                doc = documentation.objects.get(pk=request.POST['id'])
                return HttpResponse(id_input + 'Etes-vous vraiment sûr de vouloir supprimer:<br><b>'+ str(doc) + '</b><br> avec le document: <br><a href='+ doc.fichier.url + '>'+ doc.icon()+str (doc.fichier)+'</a>')
            else:
                return render(request,
                       'widgets/UpdateDocModalBody.html',
                       {
                           'id_input':id_input,
                           'classification_form': classification_form(
                               instance=documentation.objects.get(pk=request.POST['id']).classification,
                               prefix='update'
                           ),
                           'form': ajouter_procedure_form(
                               instance=documentation.objects.get(pk=request.POST['id']),
                               prefix='update'
                           ),
                       }
                       )

        #Suppression d'un fichier
        if "Supprimer" in request.POST:
            classif = documentation.objects.get(pk=request.POST['id']).classification
            documentation.objects.get(pk=request.POST['id']).delete()
            #Si la classification n'a plus de fichier , elle est supprimée
            if documentation.objects.filter(classification=classif).count() == 0:
                classif.delete()
            return redirect(request.META['HTTP_REFERER'])

        #Modification d'un fichier
        if "Modifier" in request.POST:
            class_form = classification_form(request.POST, prefix='update', instance=documentation.objects.get(pk=request.POST['id']).classification)
            if class_form.is_valid():
                if request.POST['update-titre'] == str(0):
                    class_form.save(commit=False)
                    class_form.titre = request.POST['autre']
                    classif = class_form.save()
                else:
                    classif = classification.objects.get(pk=request.POST['update-titre'])
            else:
                return render(request,
                                  self.template_name,
                                  {
                                      'title': self.title,
                                      'classification': self.c,
                                      'form': self.form(request.POST),
                                      'classification_form': classification_form(request.POST)
                                  }
                                  )
            form2 = ajouter_procedure_form(request.POST, request.FILES, prefix='update', instance=documentation.objects.get(pk=request.POST['id']))
            if form2.is_valid():
                form2.save(commit=False)
                doc = form2.save()
                doc.classification = classif
                doc.save()
            else:
                return render(request,
                              self.template_name,
                              {
                                  'title': self.title,
                                  'classification': self.c,
                                  'form': self.form(request.POST),
                                  'classification_form': classification_form(request.POST)
                              }
                              )
            return HttpResponseRedirect(reverse('sav:bibliotheque' , kwargs={'pk':documentation.objects.get(pk=request.POST['id']).classification.id}))

        #Recherche documentation
        if "key" in request.POST:
            filter= ~Q(titre__icontains="XXXXXXXX")
            for word in request.POST['key'].replace(' ', '').split(','):
                filter &= Q(titre__icontains=word)
            from .models import classification
            classi=classification.objects.filter(filter)
            html=''
            procedure=''
            i = 0
            for c in classi:
                if not c.dossier == procedure:
                    html+='<optgroup label="{}">'.format(c.sigle_toutelettre())
                html+= '<option value="{}"> {}</option>'.format(c.id, c.titre)
                if not c.dossier == procedure and i !=0:
                    html+='</optgroup>'
                i+=1
                procedure = c.dossier
            return  HttpResponse(html)

class cartcreator(View):
    login_url = '/login/'
    template_name = 'sav/cartcreator.html'
    title = "Création d'une carte de régulation"

    def get(self, request, *args, **kwargs):
        from .tasks import wrapperscapping
        installations = installation.objects.all().values('idsa')
        # from .scrapping import scrappingMySolisart
        # scrappingMySolisart().save_csv_configuration(path_csv=os.path.dirname(__file__) + '/temp/config.csv')

        return render(request,
                      self.template_name,
                      {
                          'installations':installations,
                          'title':self.title
                      }
                      )

    def post(self, request):
        if 'download' in request.POST:
            with open(os.path.dirname(__file__) + '/temp/config.csv') as myfile:
                response = HttpResponse(myfile, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=config.csv'
            return response

        if request.POST['opt'] == "json" and 'file' in request.FILES and request.POST['new_installation']:
            file = request.FILES['file']
            data = file.read()
            import json
            param = json.loads(data)

            from .tasks import wrapperscapping
            wrapperscapping.delay("cart_created_since_json", {'installation':request.POST['new_installation'], 'dict_schematic':param})

            # import os
            # from django.core.files.storage import FileSystemStorage
            #
            # #Supprime tous les fichiers du dossier temp
            # files = glob.glob(os.path.dirname(__file__) +'/temp')
            # for f in files:
            #     try:
            #         os.remove(f)
            #     except:
            #         pass
            #
            # import requests
            # from PIL import Image
            # from io import BytesIO, StringIO
            #
            # # URL de l'api
            # url = 'https://www.solisart.fr/schematics/api/getSchema.php?image=SchemaHydrauWithLegend'
            # # ici getSchema.php peut contenir 2 paramètre get :
            # #   -image : qui permet d'indiquer l'image à récupérer (SchemaHydrau, SchemaHydrauWithLegend, SchemaExe, Etiquetage, ImageFicheProg)
            # #   -format : qui peut uniquement prendre la valeur PDF pour indiquer de renvoyer l'image en format PDF
            # # exemple d'url pour récupérer l'etiquetage en format pdf :
            # #   https://www.solisart.fr/schematics/api/getSchema.php?image=Etiquetage&format=PDF
            # # dans le cas ou format n'est pas indiqué alors le téléchargement se fait en png
            #
            # # URL du fichier json qui sera envoyé
            # # le fichier json doit être une configuration téléchargé depuis la schématèque
            # # il peut être dans un ancien format cela ne devrait pas poser de problème
            #
            # # le fichier doit bien être passé avec l'identifiant 'fichier' sinon cela ne marchera pas
            # files = {'fichier': data}
            #
            # # la requête doit passé obligatoirement le fichier en paramètre files
            # response = requests.post(url, files=files)
            #
            # # Lire les données de l'image depuis la réponse
            # image_data = response.content
            # #
            # # # Créer une image à partir des données
            # image = Image.open(BytesIO(image_data))
            #
            # import os
            # #SAuvegarder dans le dossier /temp
            # image.save(os.path.dirname(__file__) +'/temp/image.png')
            #
            # # url pour récupérer la confi.csv depuis le json
            # url = 'https://www.solisart.fr/schematics/api/getConfiguration.php'
            # response = requests.post(url, files=files)
            # #Ecrit le fichier config dans le dossier tmp
            # with open(os.path.dirname(__file__) +'/temp/config.csv', 'w') as out:
            #     out.write(response.content.decode())

        elif request.POST['installation']:
            from .tasks import wrapperscapping
            wrapperscapping.delay("downloadConfigCsvInstallation", request.POST['installation'])
            param = {"valide": "OK"}
        else:
            param ={"error":"erreur dans le fichier"}

        return JsonResponse(param, safe=False)

class production(View):
    login_url = '/login/'
    template_name = 'sav/production.html'
    title = "Gestion de production"

    def get(self, request, *args, **kwargs):
        from heraklesinfo.models import C7001Phases
        excludeCL= Q(codephase__icontains='-------')
        CLs = CL_herakles.objects.all().order_by('-CL').values_list('CL', flat=True)
        for Clsolistools in CLs:
            excludeCL |=  Q(codephase__icontains=str(Clsolistools))
        heraklesCLs = C7001Phases.objects.db_manager('herakles'). \
                  filter(Q(codephase__icontains='CL' + str(timezone.now().year)[2:4]) | Q(codephase__icontains='CL' + str((timezone.now()-timedelta(days=366)).year)[2:4])). \
                  exclude(codephase__icontains='/'). \
                  exclude(excludeCL). \
                  order_by('-codephase'). \
                  values_list('codephase', flat=True)

        return render(request,
                      self.template_name,
                      {
                          'title':self.title,
                          'heraklesCLs': heraklesCLs,
                          'CLs':CLs
                      }
                      )

    def post(self, request, *args, **kwargs):
        from heraklesinfo.models import C701Ouvraof, C601ChantierEnTte
        if "numCL" in request.POST:
            numCL = request.POST['numCL']
            CLarticles = C701Ouvraof.objects.db_manager('herakles'). \
                  filter(codeof__icontains=numCL). \
                  exclude(codouv__isnull=True) .\
                  annotate(qte=Cast("nbre", output_field=(FloatField()))). \
                  order_by('codouv'). \
                  distinct(). \
                  values("codouv", "qte", "titre")
            list_codouv = [i['codouv'] for i in CLarticles]
            codechantier =  C601ChantierEnTte.objects.db_manager('herakles'). \
                  filter(t601_1_code_chantier=numCL).values('t601_12_code_client', 't601_2_titre_du_chantier', 'delai')

            capt=None
            capteur_nbre=0
            for cap in capteur.objects.all():
                if cap.type == "SID":
                    str_seach = "SI"
                else:
                    str_seach = cap.type
                if any(s.startswith(str_seach) for s in list_codouv):
                    capt = capteur.objects.get(type=str_seach)
                    for article in CLarticles:
                        if article['codouv'].startswith(str_seach):
                            capteur_nbre = int(article['codouv'][-1]) * article['qte']

            modu=None
            for mod in module.objects.all():
                if any(s.startswith(mod.type) for s in list_codouv):
                    modu = mod

            ballons=''
            for art in CLarticles:
                if art['titre'].lower().startswith("ballon-"):
                    if not ballons:
                        ballons += art['codouv']
                    else:
                        ballons += ' + ' + art['codouv']

            formCL = CL_Form(initial = {
                'CL': numCL,
                'installateur':client_herakles.objects.get(Code_Client = codechantier[0]['t601_12_code_client']),
                'information': codechantier[0]['t601_2_titre_du_chantier'],
                "capteur": capt,
                "capteur_nbre":capteur_nbre,
                "module": modu,
                "ballon": ballons,
                'date_livraison': codechantier[0]['delai']-timedelta(days=3),
                'date_livraison_prevu': codechantier[0]['delai'],
                'date_montage_prevu': codechantier[0]['delai'] - timedelta(days=15),
                'date_capteur_prevu': codechantier[0]['delai'] - timedelta(days=15),
                'date_ballon_prevu': codechantier[0]['delai'] - timedelta(days=15),
                'date_prepa_carte_prevu': codechantier[0]['delai'] - timedelta(days=7),
                'date_prepa_prevu': codechantier[0]['delai'] - timedelta(days=2),
                'date_reglement': codechantier[0]['delai'] + timedelta(days=90)
                           })

            return render(request,
                          "widgets/PresentCL.html",
                          {
                              "formCL":formCL,
                              "CLarticles":CLarticles,
                              "beforeAdd": True
                          }
                          )

        if "add_CL" in request.POST:
            form = CL_Form(data=request.POST)
            CL  = request.POST['CL']
            installateur = client_herakles.objects.get(pk=request.POST['installateur'])
            date_livraison_prevu = datetime.strptime(request.POST['date_livraison_prevu'], '%d-%m-%Y')
            if form.is_valid():
                f = form.save(commit=False)
                f.CL = CL
                f.installateur = installateur
                f.date_livraison_prevu =  date_livraison_prevu
                CL= f.save()
                send_channel_message('production', {
                    'message': "Création d'une nouvelles commande",
                    'result': [CL],
                    'datereceptionclient': False
                })
                return HttpResponseRedirect(request.path_info)
            else:
                print("error", form.errors)
            return HttpResponseRedirect(request.path_info)
        if 'calendar' in request.POST:
            # todo mettre un filter
            return JsonResponse(list([i.as_dict() for i in CL_herakles.objects.filter(
                date_reglement__gte = timezone.now() + timedelta(days=15)
    )]), safe=False)
        if 'show' in request.POST:
            CL = CL_herakles.objects.get(CL = request.POST['show'])
            formCL = CL_Form(instance=CL, show=True)

            return render(request,
                          "widgets/PresentCL.html",
                          {
                              "formCL":formCL,
                              "beforeAdd": False
                          }
                          )

        if 'update' in request.POST:
            CL1 = CL_herakles.objects.get(CL=request.POST['CL'])
            form = CL_Form(instance=CL1, data=request.POST)
            if form.is_valid():
                CL = form.save()
                send_channel_message('production', {
                    'message': "Modification de la Commande",
                    'result': [CL.CL],
                    'datereceptionclient': False
                })
                return HttpResponseRedirect(request.path_info)
            else:
                print(form.errors)

        if 'updateDate' in request.POST:
            result=[]
            for newdate in json.loads(request.POST['updateDate']):
                CL = CL_herakles.objects.get(CL=newdate['CL'])
                if 'capteur' in newdate['task']:
                    CL.date_capteur_prevu = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('capteur ' + CL.CL)
                if 'ballon' in newdate['task']:
                    CL.date_ballon_prevu = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('Ballon ' + CL.CL)
                if 'prepa' in newdate['task']:
                    CL.date_prepa_prevu = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('Prépa  ' + CL.CL)
                if 'carte' in newdate['task']:
                    CL.date_prepa_carte_prevu = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('Prépa carte ' + CL.CL)
                if 'montage' in newdate['task']:
                    CL.date_montage_prevu = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('Montage ' + CL.CL)
                if 'livraison' in newdate['task']:
                    CL.date_livraison = datetime.strptime(newdate['new'], '%Y-%m-%d')
                    result.append('Livraison ' + CL.CL)
                CL.save()


            send_channel_message('production', {
                    'message': "Modification de la Commande",
                    'result': result,
                    'datereceptionclient': False
                })


            return JsonResponse({"data":""}, safe=False)

        if 'finishTask' in request.POST:
            task = json.loads(request.POST['finishTask'])
            CL = CL_herakles.objects.get(CL=task['CL'])
            finish = datetime.strptime(task['_end'].split('T')[0], '%Y-%m-%d')
            if 'capteur' in task['id']:
                CL.date_capteur = finish
                result=['capteur ' + CL.CL]
            if 'ballon' in task['id']:
                CL.date_ballon = finish
                result=['Ballon ' + CL.CL]
            if 'prepa' in task['id']:
                CL.date_prepa = finish
                result=['Prépa ' + CL.CL]
            if 'carte' in task['id']:
                CL.date_prepa_carte = finish
                result=['Prépa carte ' + CL.CL]
            if 'montage' in task['id']:
                CL.date_montage = finish
                result=['Montage ' + CL.CL]
            if 'livraison' in task['id']:
                CL.date_livraison = finish
                result=['Livraison ' + CL.CL]
            CL.save()
            send_channel_message('production', {
                    'message': "Tâche Terminée",
                    'result': result,
                    'datereceptionclient': False
                })
            return JsonResponse({"data": ""}, safe=False)

        if 'NotFinishedTask' in request.POST:
            task = json.loads(request.POST['NotFinishedTask'])
            CL = CL_herakles.objects.get(CL=task['CL'])
            if 'capteur' in task['id']:
                CL.date_capteur = None
            if 'ballon' in task['id']:
                CL.date_ballon = None
            if 'prepa' in task['id']:
                CL.date_prepa = None
            if 'carte' in task['id']:
                CL.date_prepa_carte = None
            if 'montage' in task['id']:
                CL.date_montage = None
            if 'livraison' in task['id']:
                CL.date_livraison = None
            CL.save()
            return JsonResponse({"data": ""}, safe=False)

        if 'date_information' in request.POST:
            CLs = CL_herakles.objects.filter(date_last_update_information__gte = datetime.strptime(request.POST['date_information'],'%d-%m-%Y %H:%M'))
            html =""
            for Cl in CLs:
                html+= "<i class='fas fa-angle-right'></i><b>"+ Cl.CL +":</b><br><p>"+ Cl.information.replace('\\n', '<br>') +"</p><br>"
            return HttpResponse(html)

        return HttpResponse("error ....")
