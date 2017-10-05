from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'about', views.about, name="about"),
    url(r'cart', views.cart, name="cart"),
    url(r'faq', views.faq, name="faq"),
    url(r'^chrome/api/(?P<path>.*)$', views.proxy)
]
