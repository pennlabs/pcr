from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.form, name="form"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^reset/', views.reset_token, name="reset_token"),
]
