from django.conf.urls import url

from .views import activate, get_token, reset_token


urlpatterns = [
    url(r'^get_token/', get_token, name='get_token'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate, name='activate'),
    url(r'^reset/', reset_token, name='reset_token'),
]
