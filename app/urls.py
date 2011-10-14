from django.conf.urls.defaults import *
from django.contrib import admin

from views import *



urlpatterns = patterns('',
  (r'^instructor/(.*)$', instructor),
  (r'^department/(\w+)$', department),
  (r'^course/(\w+)-(\w+)$', course),

  (r'^browse$', browse),
  (r'^faq$', faq),
  (r'^about$', about),

  (r'^autocomplete_data.json$', autocomplete_data),
 
  (r'^$', index),
)
