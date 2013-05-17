from tastypie.resources import ModelResource
from moties.models import Motie

class MotieResource(ModelResource):
    class Meta:
        queryset = Motie.objects.all()
        allowed_methods = ['get']
