from rest_framework import serializers

from .models import ChurmHub, DataFromJujuClientTerminal

class ChurmHubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChurmHub
        fields = '__all__'

class DataFromJujuClientTerminalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataFromJujuClientTerminal
        fields = '__all__'