from django.conf import settings
from django.http import JsonResponse
from .models import APIConsumer, APIUser, generate_api_consumer
import requests

BASE_API = 'https://api.pennlabs.org'


class ShibbolethConsumer(object):
    def __init__(self, username):
        self.name = username
        self.permission_level = 2
        self.valid = True
        self.access_pcr = True
        self.access_secret = False

    def __str__(self):
        return "%s (level %d)" % (self.name, self.permission_level)


class Authenticate(object):
    """Looks up the token (passed as a GET parameter) in the token database.
    Ensures that it is a valid token, and passes the APIConsumer (i.e. user) to
    the view via request.consumer so the view knows what access level the consumer
    has."""

    def process_request(self, request):

        # We use status=403 for errors. There are HTTP status codes for
        # authentication failure, where 403 is for denied access.
        # https://en.wikipedia.org/wiki/HTTP_403

        old_path = request.path_info

        if not old_path.startswith("/api/") and settings.API_HOST not in request.META.get("HTTP_HOST", ""):
            return None

        try:
            token = request.GET['token']
        except KeyError:
            return JsonResponse({"error": "No token provided."}, status=403)

        # The reverse proxy server (Nginx, Apache) sets the REMOTE_USER variable.
        # PCR must be run using UWSGI in order to correctly receive this variable.
        # Do not use headers to validate the Shibboleth token, there are some endpoints that
        # do not have Shibboleth set up, allowing anyone to pass a header and gain access.

        if token == 'shibboleth':
            if not hasattr(request, 'environ') or not request.environ.get('REMOTE_USER'):
                consumer = None
            else:
                consumer, _ = APIUser.objects.get_or_create(username=request.environ['REMOTE_USER'].lower().split('@')[0])
        else:
            try:
                consumer = APIConsumer.objects.get(token=token)
            except APIConsumer.DoesNotExist:
                try:
                    consumer = APIUser.objects.get(token=token)
                except APIUser.DoesNotExist:
                    consumer = None

        if request.GET.get('origin', None) == 'labs-api' and not consumer:
            validation = requests.get(BASE_API + '/validate/' + token).json()
            valid = validation['status'] == 'valid'
            if valid:
                consumer = generate_api_consumer(token)

        if consumer is not None and consumer.valid:
            # The found consumer is added to the request object, in request.consumer.
            request.consumer = consumer
            return None  # continue rendering
        else:
            resp = JsonResponse({"error": "Invalid token."}, status=403)
            resp['Access-Control-Allow-Origin'] = '*'
            resp['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS',
            resp['Access-Control-Max-Age'] = 1000
            resp['Access-Control-Allow-Headers'] = '*'
            return resp
