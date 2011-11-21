from django.conf.urls.defaults import *


urlpatterns = patterns('apps.searchbar.views',
  (r'^$', 'autocomplete_data'),
)
