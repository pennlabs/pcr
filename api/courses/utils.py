import datetime

from django.http import HttpResponse

from .models import Semester


def current_semester():
    now = datetime.datetime.now()
    semester = 'A' if now.month < 5 else ('B' if now.month < 9 else 'C')
    return Semester(now.year, semester)


ACC_HEADERS = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
               'Access-Control-Max-Age': 1000,
               'Access-Control-Allow-Headers': '*'}

# allows cross-domain AJAX calls
# https://gist.github.com/1308865


def cross_domain_ajax(func):
    """ Sets Access Control request headers. """
    def wrap(request, *args, **kwargs):
        # Firefox sends 'OPTIONS' request for cross-domain javascript call.
        if request.method != "OPTIONS":
            response = func(request, *args, **kwargs)
        else:
            response = HttpResponse()
        for k, v in ACC_HEADERS.items():
            response[k] = v
        return response
    return wrap


# FNAR 337 Advanced Orange (Jaime Mundo)
# Explore the majesty of the color Orange in its natural habitat,
# and ridicule other, uglier colors, such as Chartreuse (eww).

# MGMT 099 The Art of Delegating (Alexey Komissarouky)
# The Kemisserouh delegates teaching duties to you. Independent study.

class API404(Exception):
    def __init__(self, message=None, perhaps=None):
        self.message = message
        self.perhaps = perhaps
