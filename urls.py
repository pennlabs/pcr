from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import direct_to_template


urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^', include('apps.pcr_detail.urls')),
    (r'^', include('apps.searchbar.urls')),
    (r'^', include('apps.static.urls')),
)

# Enable static file in local development
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.STATIC_DOC_ROOT}),
    )
