from rest_framework import serializers

from .models import ChurmHub

class ChurmHubSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ChurmHub
        fields = '__all__'