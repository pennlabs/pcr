from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag


register = template.Library()


@tag(register, [])
def links(context):
  new_context = {
    'base_dir': context['base_dir'] if 'base_dir' in context else ""
  }
  return render_to_string('app/templatetags/links.html', new_context)


@tag(register, [Variable()])
def choose_cols_box(context, attributes):
  #split the attributes into two columns
  cols = [attr for attr in attributes]
  new_context = {
      'left_col': cols[:len(cols)/2],
      'right_col': cols[len(cols)/2:]
  }
  return render_to_string('app/templatetags/choose_cols_box.html', new_context)
