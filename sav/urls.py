from django.urls import path, include
from django.urls import re_path as url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    path('', login_required(views.home.as_view()), name='home'),
    path('updateDB', login_required(views.updateDB.as_view()), name='updateDB'),
    path('installation/<int:pk>', login_required(views.installation_view.as_view()), name='installation'),
    path('utilisateur/<int:pk>', login_required(views.utilisateur_view.as_view()), name='utilisateur'),
    path('ticket', login_required(views.ticket_view.as_view()), name='ticket'),
    path('map', login_required(views.carte.as_view()), name='map'),
    path('statistiques', login_required(views.statistiques.as_view()), name='statistiques'),
    path('bidouille', views.bidouille.as_view(), name='bidouille')
]