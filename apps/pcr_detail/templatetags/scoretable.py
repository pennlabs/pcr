
from django import template
from django.http import Http404
from django.template.loader import render_to_string

from apps.pcr_detail.models import CourseHistory, Department, Instructor


register = template.Library()


@register.simple_tag(takes_context=True)
def scoretable(context, item):
    """
    Create a score table (the main content itself).
    """
    if type(item) == CourseHistory:
        return render_to_string('pcr_detail/templatetags/scoretable/course.html', context.flatten())
    elif type(item) == Instructor:
        return render_to_string('pcr_detail/templatetags/scoretable/instructor.html', context.flatten())
    elif type(item) == Department:
        return render_to_string('pcr_detail/templatetags/scoretable/department.html', context.flatten())
    else:
        raise Http404
