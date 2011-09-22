from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

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
  
@tag(register, [])
def choose_cols_box(context):
  return render_to_string('templates/choose_cols_box.html')