from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^', include('apps.pcr_detail.urls')),
    (r'^', include('apps.searchbar.urls')),
    (r'^', include('apps.static.urls')),
)
