from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from sandbox_config import DISPLAY_NAME


urlpatterns = patterns('',
                       (r'^$',
                        direct_to_template,
                        {'template': 'index.html',
                         'extra_context': {'base_dir': DISPLAY_NAME + '/'}
                        },
                        ),
    (r'^', include('apps.pcr_detail.urls')),
    (r'^', include('apps.searchbar.urls')),
    (r'^', include('apps.static.urls')),
)
