# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from .models import *


# Create your views here.
class home (View):
    login_url = '/login/'
    template_name = 'heraklesinfo/home.html'
    title = 'Recherche'

    def get(self, request, *args, **kwargs):
        mail = "contact@lambert-madisun.fr"
        # trouver le client avec l'adresse email
        client = C100Clients.objects.db_manager('herakles').filter(email = mail).values('t100_1_code_client')[0]['t100_1_code_client']
        #trouver toutes les chantiers affecté à ce client
        chantiers = C601ChantierEnTte.objects.db_manager('herakles').filter(t601_12_code_client=client).values_list('t601_1_code_chantier', flat=True)

        #trouver toutes les CL affectés au chantier[1]
        CLs =C7001Phases.objects.db_manager('herakles').filter(codechantier = chantiers.last())

        #trouver le BL lié au chantier [1]
        BL = C7001Phases.objects.db_manager('herakles').filter(
            codechantier = chantiers.last(),
            codephase__icontains ='BL'
        ).values('codephase')[0]['codephase']
        #article du BL
        articles = C701Ouvraof.objects.db_manager('herakles').filter(codeof = BL).values("codouv", "nbre", "titre")
        print("client", client)
        print("chantiers", chantiers)
        print('BL du dernier chantier', BL)
        for a in articles:
            print(a)



        # BL = C7001Phases.objects.db_manager('herakles').filter(codephase__icontains = 'BL').order_by('-codephase').values('codephase')[200]
        # print('BL', BL['codephase'])
        # #request pour avoir tous les articles avec un n° de BL
        # articles = C701Ouvraof.objects.db_manager('herakles').filter(codeof = 'BL23-0614').values("codouv", "nbre", "titre")
        # for a in articles:
        #     print(a)
        return render(request,
                      self.template_name,
                          {
                              'title':self.title
                          }
                      )
