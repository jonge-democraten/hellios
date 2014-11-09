from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('hellios.urls', namespace='hellios')),
    url(r'^admin/', include(admin.site.urls)),
)
