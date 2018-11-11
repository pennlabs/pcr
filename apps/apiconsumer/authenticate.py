from django.http import HttpResponse
from .models import APIConsumer, generate_api_consumer
import requests

BASE_API = 'https://api.pennlabs.org'


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

        if old_path.startswith("/admin/") or old_path.startswith("/__debug__/"):
            return None

        try:
            token = request.GET['token']
        except:
            return HttpResponse("No token provided.", status=403)

        try:
            consumer = APIConsumer.objects.get(token=token)
        except APIConsumer.DoesNotExist:
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
            return HttpResponse("Invalid token.", status=403)
