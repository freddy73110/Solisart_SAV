from django.urls import path, include
from django.urls import re_path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", login_required(views.home.as_view()), name="home"),
    re_path(r'^help/(?P<path>([^/]+/)*)$', login_required(views.Help.as_view()), name="help"),
    path("updateDB", login_required(views.updateDB.as_view()), name="updateDB"),
    path(
        "installation/<int:pk>",
        login_required(views.installation_view.as_view()),
        name="installation",
    ),
    path(
        "utilisateur/<int:pk>",
        login_required(views.utilisateur_view.as_view()),
        name="utilisateur",
    ),
    path(
        "utilisateur",
        login_required(views.utilisateur_view.as_view()),
        name="AjoutUtilisateur",
    ),    
    path("ticket", login_required(views.ticket_view.as_view()), name="ticket"),
    path("map", login_required(views.carte.as_view()), name="map"),
    path(
        "bibliotheque",
        login_required(views.bibliotheque.as_view()),
        name="bibliotheque",
    ),
    path(
        "bibliotheque/<int:pk>",
        login_required(views.bibliotheque.as_view()),
        name="bibliotheque",
    ),
    path(
        "statistiques",
        login_required(views.statistiques.as_view()),
        name="statistiques",
    ),
    # path('mail', login_required(views.mail.as_view()), name='mail'),
    path("bidouille", views.bidouille.as_view(), name="bidouille"),
    path(
        "cartcreator", login_required(views.cartcreator.as_view()), name="cartcreator"
    ),
    path(
        "cartcreator/installation/<int:pkinstal>",
        login_required(views.cartcreator.as_view()),
        name="cartcreator",
    ),
    path(
        "cartcreator/<int:pkCL>",
        login_required(views.cartcreator.as_view()),
        name="cartcreator",
    ),
    
    path("production/<int:pkCL>", login_required(views.production.as_view()), name="productionwithCL"),
    path("production", login_required(views.production.as_view()), name="production"),
    path("tools", login_required(views.tools.as_view()), name="tools"),
    path("tool2", login_required(views.tool2.as_view()), name="tool2"),
    path(
        "tools/<int:pk_instal>/<slug:date>",
        login_required(views.tools.as_view()),
        name="tools",
    ),
    path("bg_dark", login_required(views.bg_dark), name="bg_dark"),
    path("assembly/<int:pkCL>", login_required(views.assemblyView.as_view()), name="assembly"),
    path("batch", login_required(views.batchView.as_view()), name="batch")
]
