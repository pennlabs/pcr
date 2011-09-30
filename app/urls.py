from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
  (r'^instructor$', instructor),
  (r'^department(\w{4})$', department),
  (r'^course/(\w+)$', course),

  (r'^browse$', browse),
  (r'^faq$', faq),
  (r'^about$', about),
 
  (r'^$', index),
)
