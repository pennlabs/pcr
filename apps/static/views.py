import mimetypes

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render


def about(request):
    return render(request, 'about.html')


def faq(request):
    return render(request, 'faq.html')


def cart(request):
    return render(request, 'cart.html')


def logout(request):
    return redirect('https://idp.pennkey.upenn.edu/logout')


def proxy(request, path):
    if not settings.PROXY_TOKEN:
        return HttpResponse('No proxy token set in settings.py!', status=500, mimetype='text/plain')

    url = '%s%s' % (settings.DOMAIN, path)
    try:
        proxied_request = requests.get(url, params={'token': settings.PROXY_TOKEN})
        proxied_request.raise_for_status()
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.text
        return HttpResponse(content, status=proxied_request.status_code, mimetype=mimetype)
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500, mimetype='text/plain')
