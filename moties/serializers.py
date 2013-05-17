from rest_framework import serializers
from moties.models import Motie

class MotieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Motie
        fields = ('titel','content','status','indiener','woordvoerder',
                'indiendatum','datum')
