from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
  (r'^instructor$', instructor),
  (r'^department$', department),
  (r'^course$', course),
  (r'^browse$', browse),

  (r'^faq$', faq),
  (r'^about$', about),
 
  (r'^$', index),
)
