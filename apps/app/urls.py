from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
  (r'^instructor/(.*)$', instructor),
  (r'^course/(\w+)-(\w+)$', course),

  (r'^(faq)/$', static),
  (r'^(about)/$', static),

  (r'^autocomplete_data.json$', autocomplete_data),
 
  (r'^$', index),
)
