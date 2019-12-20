import requests
from django import template
from django.http import Http404
from django.template.loader import render_to_string

from ..models import CourseHistory, Department, Instructor


register = template.Library()


@register.simple_tag(takes_context=True)
def infobox(context, item):
    """
    Create a scorecard.
    """
    if type(item) == CourseHistory:
        new_context = {
            'title': context['title'],
            'aliases': item.aliases - set([context['title']]),
            'coursehistory': item,
        }
        return render_to_string('pcr_detail/templatetags/infobox/course.html', new_context)
    elif type(item) == Instructor:
        email = None
        try:
            r = requests.get(
                'https://api.pennlabs.org/directory/search', params={'name': item.name})
            r.raise_for_status()
            if len(r.json()['result_data']) == 1:
                email = r.json()['result_data'][0]['list_email'].lower()
        except requests.exceptions.RequestException:
            pass
        new_context = {
            'instructor': item,
            'email': email,
        }
        return render_to_string('pcr_detail/templatetags/infobox/instructor.html', new_context)
    elif type(item) == Department:
        new_context = {
            'department': item,
        }
        return render_to_string('pcr_detail/templatetags/infobox/department.html', new_context)
    else:
        raise Http404
