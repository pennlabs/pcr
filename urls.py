from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path

from api.search.views import search


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search', search),
    url(r'^api/', include('api.courses.urls', namespace='api')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
