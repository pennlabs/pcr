from django.http import JsonResponse

from lib.api import api


def autocomplete_data(request, start=None):
    """Generate an autocomplete_data.json file, with an optional search
    string `start` (usually two characters)."""

    return JsonResponse(api('display', 'autocomplete'))
