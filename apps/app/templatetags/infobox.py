from collections import namedtuple

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from average import average


register = template.Library()


@tag(register, [Variable()])
def infobox(context, item):
  '''Create a scorecard.'''
  new_context = {
    'scorecard': None
    }
  return render_to_string('templatetags/scorecard.html', new_context)
