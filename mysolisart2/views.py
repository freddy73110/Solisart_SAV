from django.views import View
from django.shortcuts import render

class installation (View):
    template_name = 'mysolisart2/installation.html'
    title = 'Recherche'

    def get(self, request, *args, **kwargs):
        return render(request,
                      self.template_name
                      )
