from django.conf.urls import url, include
from django.views.generic import DetailView, ListView
from hellios.models import Motie
from hellios.views import *

urlpatterns = [
    url(r'^$', view_home, name='home'),
    url(r'^list/$', MotieListView.as_view(), name='motie-list'),
    url(r'^tag/(?P<tag>.+)/$', TagView.as_view(), name='tag'),
    url(r'^tags/$', TagListView.as_view(), name='tag-list'),
    url(r'^motie/(?P<pk>\d+)/$', MotieView.as_view()),
    url(r'^motie/(?P<pk>\d+)/(?P<slug>[-\w\d]*)/$', MotieView.as_view(), name='motie'),
    url(r'^standpunten/(?P<letter>[A-Z])/$', view_standpunten, name='standpunten'),
    url(r'^programma/(?P<pk>\d+)/$', ProgrammaView.as_view(), name='programma'),
    url(r'^programma/$', view_default_programma, name='default_programma'),
    url(r'^programma/hoofdstuk/(?P<hoofdstuk>\d+)/$', view_default_programma_hoofdstuk, name='default_hoofdstuk'),
]
