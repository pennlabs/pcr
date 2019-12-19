from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

from api.search.views import search


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^', include('apps.pcr_detail.urls')),
    url(r'^', include('apps.searchbar.urls')),
    url(r'^', include('apps.static.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^search', search),
    url(r'^api/', include('api.courses.urls', namespace='api')),
]
