from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from sav.serializers import (
    GroupSerializer,
    UserSerializer,
    InstallationSerializer,
    FichierSerializer,
    TicketSerializer,
    NCSerializer,
)
from rest_framework.response import Response

from .models import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class InstallationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = installation.objects.all()
    serializer_class = InstallationSerializer
    lookup_field = 'idsa'

    @action(detail=True, methods=['get'])
    def coordonnee(self, request, idsa=None):
        installation = self.get_object()
        return Response(installation.GEOlist())


class FichierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Fichiers.objects.all()
    serializer_class = FichierSerializer
    permission_classes = [permissions.IsAuthenticated]


class TicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


class NCViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = noncompliance.objects.all()
    serializer_class = NCSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
