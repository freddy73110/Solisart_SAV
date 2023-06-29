# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ModelAdmin

from .models import *

# Register your models here.

class Allinstallateur(SimpleListFilter):
    title = 'Tous les installateurs' # or use _('country') for translated title
    parameter_name = 'installatezur'

    def lookups(self, request, model_admin):
        states = ['Tous','Administrateur', 'Technicien', 'Installateur', 'Propriétaire']
        return [(c, c) for c in states]

    def queryset(self, request, queryset):
        from .models import acces
        if self.value() == "Tous" or not self.value():
            return queryset.all()
        else:
            acces = acces.objects.filter(profil_type__name = self.value()).values_list('utilisateur__id', flat=True).distinct()
            return queryset.filter(user__id__in = acces)

class profil_user_Admin(ModelAdmin):
    list_display = ('user', 'Client_herakles')
    list_display_links = None
    list_editable = ('Client_herakles',)
    list_filter = (Allinstallateur,)


admin.site.register(profil_user,profil_user_Admin)
admin.site.register(profil_type)
admin.site.register(installation)
admin.site.register(acces)
admin.site.register(attribut_def)
admin.site.register(attribut_valeur)
admin.site.register(probleme)
admin.site.register(ticket)
admin.site.register(evenement)
admin.site.register(Fichiers)
admin.site.register(historique)
admin.site.register(donnee)
admin.site.register(cause)
admin.site.register(MES)
admin.site.register(documentation)
admin.site.register(classification)
admin.site.register(BL_herakles)
admin.site.register(devis_herakles)
admin.site.register(client_herakles)
admin.site.register(solution)
# admin.site.register(attachement)
