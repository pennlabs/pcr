from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import mimetypes
import urllib2

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


def proxy(request, path):
    url = '%s%s%s%s' % (settings.DOMAIN, path, '?token=', settings.PROXY_TOKEN)
    try:
        proxied_request = urllib2.urlopen(url)
        status_code = proxied_request.code
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.read()
    except urllib2.HTTPError as e:
        return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
