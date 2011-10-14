from django.conf.urls.defaults import *

from app import urls


urlpatterns = patterns('',
    # Example:
    # (r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^', include(urls)),
)
