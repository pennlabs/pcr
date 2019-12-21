from django.conf import settings
from django.utils.cache import patch_vary_headers


class ApiHostMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            host = request.META['HTTP_HOST'].rsplit(':', 1)[0]
            if host == settings.API_HOST:
                request.urlconf = 'api.urls'
        except KeyError:
            pass

        response = self.get_response(request)

        if getattr(request, 'urlconf', None):
            patch_vary_headers(response, ('Host',))

        return response
