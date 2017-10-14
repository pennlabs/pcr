from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^instructor/(.*)$', views.instructor),
    url(r'^course/(\w+)-(\w+)$', views.course),
    url(r'^department/(\w+)$', views.department),
]
