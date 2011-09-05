from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

@tag(register, [])
def links(context):
  return render_to_string('templates/links.html')
