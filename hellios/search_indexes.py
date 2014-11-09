import datetime
from haystack import indexes
from hellios.models import *

class MotieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    status = indexes.CharField(model_attr='status')
    
    def get_model(self):
        return Motie

    def index2_queryset(self, using=None):
        return self.get_model().objects.all().exclude(status__exact=Motie.INGEDIEND)
