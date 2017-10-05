from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from models import Instructor, CourseHistory, Department


def instructor(request, id):
  instructor = Instructor(id)
  context = {
    'item': instructor,
    'reviews': instructor.reviews,
    'title': instructor.name,
    'show_name': True,
    'type': 'instructor',
  }
  return render(request, 'pcr_detail/detail.html', context)


def course(request, dept, id):
  title = '%s-%s' % (dept.upper(), id)
  coursehistory = CourseHistory(title)
  reviews = set(review for course in coursehistory.courses for section in course.sections for review in section.reviews)
  context = {
    'item': coursehistory,
    'reviews': reviews,
    'show_name': len(set([r.section.name for r in reviews])) != 1,
    'title': title,
    'type': 'course',
  }
  return render(request, 'pcr_detail/detail.html', context)


def department(request, name):
  department = Department(name)
  context = {
    'item': department,
    'reviews': set(review for coursehistory in department.coursehistories
                    for course in coursehistory.courses
                    for section in course.sections
                    for review in section.reviews),
    'title': name,
    'show_name': True,
    'type': 'department',
  }
  return render(request, 'pcr_detail/detail.html', context)
