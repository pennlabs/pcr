from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'(about)', 'apps.static.views.static'),
    (r'(faq)', 'apps.static.views.static'),
    (r'^chrome/api/(?P<path>.*)$', 'apps.static.views.proxy'),

)

