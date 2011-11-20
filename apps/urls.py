from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'^autocomplete_data.json$', include('apps.searchbar.urls')),
    (r'^', include('apps.app.urls')),
)
