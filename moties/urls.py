from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView
from moties.models import Motie
from moties.views import MotieDetailView
from moties.views import MotieList, MotieDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('moties.views',
    url(r'^$',
        ListView.as_view(
            queryset=Motie.objects.order_by('-datum'),
            context_object_name='moties',
            template_name='moties/index.html'), name='index'),
    url(r'^(?P<pk>\d+)/$', 
        MotieDetailView.as_view(
            model=Motie,
            template_name='moties/detail.html'), name='detail'),
    url(r'^api/$', 'api_root'),
    url(r'^api/moties/$', MotieList.as_view(), name='motie-list'),
    url(r'^api/moties/(?P<pk>\d+)/$', MotieDetail.as_view(), name='motie-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])

