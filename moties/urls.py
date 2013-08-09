from django.conf.urls import patterns, url, include
from django.views.generic import DetailView, ListView
from moties.models import Motie
from moties.views import *
from moties import views
# from rest_framework import routers

#router = routers.DefaultRouter()
#router.register(r'moties', views.MotieViewSet)

urlpatterns = patterns('moties.views',
    #url(r'^', include(router.urls)),
    url(r'^$', views.view_home, name='home'),
    url(r'^list/$', MotieListView.as_view(), name='motie-list'),
    url(r'^tag/(?P<tag>.+)/$', TagView.as_view(), name='tag'),
    url(r'^tags/$', TagListView.as_view(), name='tag-list'),
    url(r'^motie/(?P<pk>\d+)/$', MotieView.as_view()),
    url(r'^motie/(?P<pk>\d+)/(?P<slug>[-\w\d]*)/$', MotieView.as_view(), name='motie'),
    url(r'^standpunten/(?P<letter>[A-Z])/$', views.view_standpunten, name='standpunten'), 
    url(r'^programma/(?P<pk>\d+)/$', ProgrammaView.as_view(), name='programma'),
    url(r'^programma/$', views.view_default_programma, name='default_programma'),
    # url(r'^search/', include('haystack.urls')),
)
