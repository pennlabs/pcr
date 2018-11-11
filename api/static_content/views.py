from .models import Page
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from ..json_helpers import JSON


@never_cache
def serve_page(request, page):
    # TODO here - what if you can't find it? give some interesting error
    page = Page.objects.get(name=page.strip('/'))
    return JSON(page.content)
