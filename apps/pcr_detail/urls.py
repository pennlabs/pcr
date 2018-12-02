from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^instructor/(.*)$', views.instructor, name="instructor"),
    url(r'^course/(\w+-\w+)$', views.course, name="course"),
    url(r'^department/(\w+)$', views.department, name="department"),
    url(r'live/(\w+-\w+)$', views.live, name="live"),
]
