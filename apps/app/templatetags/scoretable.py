from collections import namedtuple

from django import template
from django.http import Http404
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from apps.app.models import CourseHistory, Instructor


register = template.Library()


@tag(register, [Variable()])
def scoretable(context, item):
  '''Create a scorecard.'''
  if type(item) == CourseHistory:
    return render_to_string('app/templatetags/scoretable/course.html', context)
  elif type(item) == Instructor:
    return render_to_string('app/templatetags/scoretable/instructor.html', context)
  else:
    raise Http404
