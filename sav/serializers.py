from django.contrib.auth.models import Group, User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups', 'id']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

 
from .models import *
 
# create a serializer class
class InstallationSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = installation
        fields = ('id', 'idsa')

class FichierSerializer(serializers.ModelSerializer):
 
    # create a meta class
    class Meta:
        model = Fichiers
        fields = "__all__"

class TicketSerializer(serializers.ModelSerializer):

    instal = serializers.CharField(source='evenement.installation')
 
    # create a meta class
    class Meta:
        model = ticket
        fields = "__all__"

class NCSerializer(serializers.ModelSerializer):

    date = serializers.DateTimeField(source='ticket.evenement.date')

    # create a meta class
    class Meta:
        model = noncompliance
        fields = "__all__"