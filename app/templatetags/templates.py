from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

from prettify import PRETTIFY_REVIEWBITS

register = template.Library()

@tag(register, [])
def links(context):
  return render_to_string('templates/links.html')
  
@tag(register, [])
def searchbar(context):
  return render_to_string('templates/searchbar.html')
  
@tag(register, [])
def content_settings(context):
  return render_to_string('templates/content_settings.html')
  
@tag(register, [Variable()])
def choose_cols_box(context, fields):
  half = len(fields)/2+1
  new_context = {
    'fields0': fields[2:half],
    'fields1': fields[half:-1]
  }
  return render_to_string('templates/choose_cols_box.html', new_context)
