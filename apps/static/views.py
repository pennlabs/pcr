from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import mimetypes

from lib.api import api


def static(request, page):
    context = {
        'content': api('pcrsite-static', page)
    }
    return render(request, 'static.html', context)


def about(request):
    return static(request, "about")


def faq(request):
    return static(request, "faq")


def cart(request):
    return static(request, "cart")


def logout(request):
    return redirect("https://idp.pennkey.upenn.edu/logout")


def proxy(request, path):
    url = '%s%s' % (settings.DOMAIN, path)
    try:
        proxied_request = requests.get(url, params={"token": settings.PROXY_TOKEN})
        proxied_request.raise_for_status()
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.text
    except requests.exceptions.RequestException as e:
        return HttpResponse(str(e), status=500, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
