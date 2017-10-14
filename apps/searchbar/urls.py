from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'autocomplete_data.json/(.*)', views.autocomplete_data),
]
