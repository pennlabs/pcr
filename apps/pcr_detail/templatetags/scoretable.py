from collections import namedtuple

from django import template
from django.http import Http404
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from apps.pcr_detail.models import CourseHistory, Instructor, Department


register = template.Library()


@tag(register, [Variable()])
def scoretable(context, item):
  '''Create a score table (the main content itself).'''
  if type(item) == CourseHistory:
    return render_to_string('pcr_detail/templatetags/scoretable/course.html', context)
  elif type(item) == Instructor:
    return render_to_string('pcr_detail/templatetags/scoretable/instructor.html', context)
  elif type(item) == Department:
    return render_to_string('pcr_detail/templatetags/scoretable/department.html', context)
  else:
    raise Http404
