from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

class Table(object):
  def __init__(self, head, fields,  body):
    self.head = zip(fields, head)
    self.body = [zip(fields, row) for row in body]



@tag(register, [Variable()])
def course_table(context, table):
  '''Create a table.'''
  new_context = {
    'table': table,
    'instructor': context['instructor'] if 'instructor' in context else None
  }
  return render_to_string('templates/course_table.html', new_context)

@tag(register, [Variable(), Variable()])
def section_table(context, table, row_id):
  '''Create a table.'''
  new_context = {
    'table': table,
    'row_id': row_id
  }
  return render_to_string('templates/section_table.html', new_context)
