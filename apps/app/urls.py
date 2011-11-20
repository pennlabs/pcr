from django.conf.urls.defaults import *


urlpatterns = patterns('apps.app.views',
  (r'^instructor/(.*)$', 'instructor'),
  (r'^course/(\w+)-(\w+)$', 'course'),
)
