from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'autocomplete_data.json', 'apps.searchbar.views.autocomplete_data'),
    (r'(about)', 'apps.static.views.static'),
    (r'(faq)', 'apps.static.views.static'),
    (r'^', include('apps.pcr_detail.urls')),
)
