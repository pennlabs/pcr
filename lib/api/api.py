import functools

import requests
from django.conf import settings

from api.apiconsumer.models import APIConsumer


@functools.lru_cache(maxsize=32768)
def api(domain, *args, **kwargs):
    if 'token' not in kwargs:
        consumer = APIConsumer.objects.filter(permission_level__gte=2).first()
        if consumer is not None:
            kwargs['token'] = consumer.token
    assert domain.endswith('/')
    path = ''.join(
        (domain, '/'.join([str(arg) for arg in args])))
    try:
        response = requests.get(path, params=kwargs)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise ValueError('invalid server response: {}'.format(e.response.status_code))
    except requests.exceptions.RequestException:
        raise ValueError('invalid path: {}'.format(path))

    resp = response.json()

    if 'result' in resp:
        return resp['result']
    return resp


api = functools.partial(api, settings.DOMAIN)
