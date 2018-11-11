from django.conf.urls import url, include
from django.conf import settings

from api.static_content.views import serve_page
from api.search.views import search

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Example:

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', admin.site.urls),
    url(r'^pcrsite-static/(?P<page>.*)$', serve_page),
    url(r'^search', search),
    url(r'^' + settings.DISPLAY_NAME.lstrip("/"), include("api.courses.urls")),
]
