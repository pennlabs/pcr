from django.conf.urls.defaults import *


urlpatterns = patterns('',
    (r'(about)', 'apps.static.views.static'),
    (r'(faq)', 'apps.static.views.static'),
)
