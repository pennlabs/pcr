from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext


def instructor(request, id):
  from models import Instructor
  instructor = Instructor(id)
  context = RequestContext(request, {
    'base_dir': '../',
    'item': instructor,
    'reviews': instructor.reviews,
    'title': instructor.name,
    'type': 'instructor',
  })
  return render_to_response('pcr_detail/detail.html', context)


def course(request, dept, id):
  from models import CourseHistory
  title = '%s-%s' % (dept.upper(), id)
  coursehistory = CourseHistory(title)
  context = RequestContext(request, {
    'base_dir': '../',
    'item': coursehistory,
    'reviews': set(review for course in coursehistory.courses for section in course.sections for review in section.reviews),
    'title': title,
    'type': 'course',
    })
  return render_to_response('pcr_detail/detail.html', context)


def department(request, name):
  from models import Department
  department = Department(name)
  context = RequestContext(request, {
    'base_dir': '../',
    'item': department,
    'reviews': set(review for coursehistory in department.coursehistories 
                    for course in coursehistory.courses 
                    for section in course.sections 
                    for review in section.reviews),
    'title': name,
    'type': 'department',
  })  
  return render_to_response('pcr_detail/detail.html', context)
