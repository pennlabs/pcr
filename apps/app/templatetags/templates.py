from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

from prettify import PRETTIFY_REVIEWBITS

register = template.Library()

@tag(register, [])
def links(context):
  new_context = {
    'base_dir': context['base_dir'] if 'base_dir' in context else ""
  }
  return render_to_string('templatetags/links.html', new_context)
  
@tag(register, [])
def searchbar(context):
  return render_to_string('templatetags/searchbar.html')
  
@tag(register, [Variable()])
def choose_cols_box(context, fields):
  half = (len(fields)-3)/2+3
  new_context = {
    'fields0': fields[3:half],
    'fields1': fields[half:-1]
  }
  return render_to_string('templatetags/choose_cols_box.html', new_context)

@tag(register, [])
def tutorial_overlay(context):
  return render_to_string('templatetags/tutorial_overlay.html')
