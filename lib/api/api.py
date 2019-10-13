import functools
import requests
import json

from django.conf import settings

from api.apiconsumer.models import APIConsumer


@functools.lru_cache(maxsize=32768)
def api(domain, *args, **kwargs):
    if not "token" in kwargs:
        kwargs["token"] = APIConsumer.objects.filter(permission_level__gte=2).first().token
    assert domain.endswith("/")
    path = "".join(
        (domain, "/".join([str(arg) for arg in args])))
    try:
        response = requests.get(path, params=kwargs)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError("invalid server response: {}".format(e.response.status_code))
    except requests.exceptions.RequestException:
        raise ValueError("invalid path: {}".format(path))

    resp = response.json()

    if 'result' in resp:
        return resp['result']
    return resp


api = functools.partial(api, settings.DOMAIN)
