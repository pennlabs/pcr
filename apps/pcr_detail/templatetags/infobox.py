from collections import namedtuple

from django import template
from django.http import Http404
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from apps.pcr_detail.models import CourseHistory, Instructor


register = template.Library()


@tag(register, [Variable()])
def infobox(context, item):
  '''Create a scorecard.'''
  if type(item) == CourseHistory:
    new_context = {
      'title': context['title'],
      'aliases': item.aliases - set([context['title']]),
      'coursehistory': item,
      }
    return render_to_string('pcr_detail/templatetags/infobox/course.html', new_context)
  elif type(item) == Instructor:
    new_context = {
      'instructor': item,
      }
    return render_to_string('pcr_detail/templatetags/infobox/instructor.html', new_context)
  else:
    raise Http404
