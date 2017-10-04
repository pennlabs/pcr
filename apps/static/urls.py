from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'(about)', views.static),
    url(r'(cart)', views.static),
    url(r'(faq)', views.static),
    url(r'^chrome/api/(?P<path>.*)$', views.proxy)
]
