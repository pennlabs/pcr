from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^', include('apps.pcr_detail.urls')),
    url(r'^', include('apps.searchbar.urls')),
    url(r'^', include('apps.static.urls')),
]

# Enable static file in local development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_DOC_ROOT)
