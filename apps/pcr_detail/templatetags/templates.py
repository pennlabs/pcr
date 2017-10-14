from django import template
from django.template.loader import render_to_string


register = template.Library()


@register.simple_tag(takes_context=True)
def links(context):
  new_context = {
  }
  return render_to_string('pcr_detail/templatetags/links.html', new_context)


@register.simple_tag(takes_context=True)
def choose_cols_box(context, attributes):
  #split the attributes into two columns
  cols = [attr for attr in attributes]
  half = len(cols)/2+1
  new_context = {
      'left_col': cols[:half],
      'right_col': cols[half:]
  }
  return render_to_string('pcr_detail/templatetags/choose_cols_box.html', new_context)
