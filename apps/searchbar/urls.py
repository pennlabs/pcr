from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'autocomplete_data.json', 'apps.searchbar.views.autocomplete_data'),
)

