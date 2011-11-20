from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext



def instructor(request, id):
  from models import Instructor
  context = RequestContext(request, {
    'instructor': Instructor(id),
    'base_dir': '../'
  })
  return render_to_response('instructor.html', context)


def course(request, dept, id):
  from models import CourseHistory
  context = RequestContext(request, {
    'course': CourseHistory('%s-%s' % (dept.upper(), id)),
    'base_dir': '../'
    })
  return render_to_response('course.html', context)
