from django.shortcuts import render_to_response
from django.http import HttpResponse
import mimetypes
import urllib2

from pcrsite.lib.api import api


def static(request, page):
  context = {
    'base_dir': './',
    'content': api('pcrsite-static', page)
    }
  return render_to_response('static.html', context)



def proxy(request, path):
    url = '%s%s%s' % ('http://api.penncoursereview.com/v1/', path, '?token=smOFfjV6JeHUgGO5e7VdEAYuF3oQGn')
    try:
        proxied_request = urllib2.urlopen(url)
        status_code = proxied_request.code
        mimetype = proxied_request.headers.typeheader or mimetypes.guess_type(url)
        content = proxied_request.read()
    except urllib2.HTTPError as e:
        return HttpResponse(e.msg, status=e.code, mimetype='text/plain')
    else:
        return HttpResponse(content, status=status_code, mimetype=mimetype)
