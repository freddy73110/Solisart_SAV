# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, ModelAdmin

from .models import *

class B50ComposantsAdmin(ModelAdmin):
    using = 'herakles'
    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(B50ComposantsAdmin, self).get_queryset(request).using(self.using)

admin.site.register(B50Composants, B50ComposantsAdmin)
