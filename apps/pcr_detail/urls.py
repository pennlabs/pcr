from django.conf.urls.defaults import *


urlpatterns = patterns('apps.pcr_detail.views',
  (r'^instructor/(.*)$', 'instructor'),
  (r'^course/(\w+)-(\w+)$', 'course'),
  (r'^department/(\w+)$', 'department'),
)
