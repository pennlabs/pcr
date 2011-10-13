from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
  (r'^instructor/(.*)$', instructor),
  (r'^department/(\w+)$', department),
  (r'^course/(\w+)-(\w+)$', course),

  (r'^browse$', browse),
  (r'^faq$', faq),
  (r'^about$', about),
 
  (r'^$', index),
)
