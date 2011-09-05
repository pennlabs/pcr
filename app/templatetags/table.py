from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()

class Table(object):
  def __init__(self, head, body, width):
    self.head = head
    self.body = [zip(head, row) for row in body]
    self.width = width

@tag(register, [Variable(), Variable()])
def course_table(context, width, table):
  '''Create a table.'''
  new_context = {
    'table': table
  }
  return render_to_string('templates/course_table.html', new_context)

@tag(register, [Variable(), Variable()])
def section_table(context, width, table):
  '''Create a table.'''
  new_context = {
    'table': table
  }
  return render_to_string('templates/section_table.html', new_context)
