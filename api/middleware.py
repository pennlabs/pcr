from django.conf import settings
from django.utils.cache import patch_vary_headers


class ApiHostMiddleware():
    def process_request(self, request):
        try:
            host = request.META["HTTP_HOST"].rsplit(":", 1)[0]
            if host == settings.API_HOST:
                request.urlconf = "api.urls"
        except KeyError:
            pass

    def process_response(self, request, response):
        if getattr(request, "urlconf", None):
            patch_vary_headers(response, ('Host',))
        return response
