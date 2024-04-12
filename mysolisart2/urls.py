from django.urls import path, include
from django.urls import re_path as url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('installation', login_required(views.installation.as_view()), name='installation'),
]