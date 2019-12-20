from django.conf.urls import include, url

from .courses.views import instructor_main


urlpatterns = [
    url(r'^(?:v1/)?', include('api.courses.urls', namespace='api')),
    url(r'^instructor/(.*)$', instructor_main, name='instructor'),
]
