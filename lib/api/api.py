import functools
import requests
import json

from django.conf import settings


@functools.lru_cache(maxsize=None)
def api(domain, *args, **kwargs):
    assert domain.endswith("/")
    path = "".join(
        (domain, "/".join([str(arg) for arg in args])))
    try:
        response = requests.get(path, params=kwargs)
    except Exception:
        raise ValueError("invalid path: %s", path)
    return response.json()['result']


api = functools.partial(api, settings.DOMAIN, token=settings.PCR_API_TOKEN)
