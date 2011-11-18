from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
  (r'^autocomplete_data.json$', autocomplete_data),
)
