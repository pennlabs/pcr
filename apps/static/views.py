from django.shortcuts import render_to_response

from api import api


def static(request, page):
  context = {
    'base_dir': './',
    'content': api('pcrsite-static', page)
    }
  return render_to_response('static.html', context)
