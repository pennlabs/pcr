from django.conf.urls import include, url

urlpatterns = [
    url(r'^', include('api.courses.urls', namespace='api')),
]
