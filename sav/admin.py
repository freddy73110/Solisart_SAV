# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ModelAdmin

from .models import *
import csv
from heraklesinfo.models import B50Composants

# Register your models here.

def exportCSV(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="listArticlesuivi.csv"'
    writer = csv.writer(response)
    writer.writerow(['Ref', 'nom'])
    rows = queryset
    for row in rows:
        try:
            writer.writerow([row.name, B50Composants.objects.db_manager("herakles").get(t50_2_code_comp = row.name).t50_37_titre_du_composant])
        except:
            print("no")
    return response
exportCSV.short_description = 'Export to csv'


class Allinstallateur(SimpleListFilter):
    title = "Tous les installateurs"  # or use _('country') for translated title
    parameter_name = "installateur"

    def lookups(self, request, model_admin):
        states = [
            "Tous",
            "Administrateur",
            "Technicien",
            "Installateur",
            "Propriétaire",
            "Localisé",
        ]
        return [(c, c) for c in states]

    def queryset(self, request, queryset):
        from .models import acces

        if self.value() == "Tous" or not self.value():
            return queryset.all()
        elif self.value() == "Localisé":
            return queryset.filter(latitude__isnull=False)
        else:
            acces = (
                acces.objects.filter(profil_type__name=self.value())
                .values_list("utilisateur__id", flat=True)
                .distinct()
            )
            return queryset.filter(user__id__in=acces)


class profil_user_Admin(ModelAdmin):
    list_display = ("user", "Client_herakles", "latitude", "longitude")
    search_fields = ["user__last_name", "user__first_name"]
    list_filter = (Allinstallateur,)


class CL_HeraklesAdmin(admin.ModelAdmin):
    list_display = ("CL", "module", "installation")
    search_fields = ["CL"]


class installationAdmin(admin.ModelAdmin):
    search_fields = ["idsa"]


class fichiersAdmin(admin.ModelAdmin):
    search_fields = ["titre"]

class tracability_organAdmin(admin.ModelAdmin):
    actions = [exportCSV]


admin.site.register(profil_user, profil_user_Admin)
admin.site.register(profil_type)
admin.site.register(installation, installationAdmin)
admin.site.register(acces)
admin.site.register(attribut_def)
admin.site.register(attribut_valeur)
admin.site.register(probleme)
admin.site.register(ticket)
admin.site.register(evenement)
admin.site.register(Fichiers, fichiersAdmin)
admin.site.register(historique)
admin.site.register(donnee)
admin.site.register(cause)
admin.site.register(MES)
admin.site.register(documentation)
admin.site.register(classification)
admin.site.register(BL_herakles)
admin.site.register(devis_herakles)
admin.site.register(client_herakles)
admin.site.register(CL_herakles, CL_HeraklesAdmin)
admin.site.register(solution)
admin.site.register(module)
admin.site.register(capteur)
admin.site.register(transporteur)
admin.site.register(critere)
admin.site.register(evaluation)
admin.site.register(noncompliance)
admin.site.register(validationModule)
admin.site.register(assembly)
admin.site.register(tracability_organ, tracability_organAdmin)
admin.site.register(tracability)
admin.site.register(batch)
