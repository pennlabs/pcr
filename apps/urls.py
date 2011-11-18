from django.conf.urls.defaults import *

import app.urls
import searchbar.urls


urlpatterns = patterns('',
    # Example:
    # (r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),


    (r'^autocomplete_data.json$', include(searchbar.urls)),
    (r'^', include(app.urls)),
)
