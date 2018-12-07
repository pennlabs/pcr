"""
This module contains helper functions for responding with JSON data.
"""
import datetime
import json

from django.http import HttpResponse

from django.conf import settings


def JSON(result, valid=True, httpstatus=200):
    """
    Return a HttpResponse whose content is filled with the result of calling
    `json.dumps` with `result` and standard meta-data.
    """
    content = json.dumps({"result": result,
                          "valid": valid,
                          "version": "0.3",
                          "retrieved": str(datetime.datetime.now())},
                         sort_keys=True,
                         indent=3)
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        content = "<html><body>%s</body></html>" % content
    return HttpResponse(status=httpstatus,
                        content=content,
                        content_type="application/json")
