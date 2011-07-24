from collections import namedtuple

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.scorecard_tag import ScoreCard, ScoreBoxRow, ScoreBox
from templatetags.table import Table
from coursereview import Department, Course, Instructor

def index(request):
  return render_to_response('index.html')

def instructor(request):
  name = 'Mitch Marcus'
  title = 'Professor of Computational Linguistics'
  address = '503 Levine'
  phone = '267-702-5780'
  email = 'marcus@cis.upenn.edu'
  instructor = Instructor(name, title, address, phone, email)

  field_names = ['Class', 'Course', 'Instructor', 'Difficulty']
  Row = namedtuple('Row', field_names)
  row1 = Row('CIS 110', 3, 5, 3)
  row2 = Row('CIS 121', 3, 6, 4)
  score_table = Table(field_names, [row1, row2], 12)
  
  sb_course = ScoreBox('Course', 8)
  sb_instructor = ScoreBox('Instructor', 5)
  sb_difficulty = ScoreBox('Difficulty', 7)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row = ScoreBoxRow('Average', '70 sections', boxes)
  scorecard = ScoreCard([sb_row])

  context = RequestContext(request, {
    'instructor': instructor,
    'score_table': score_table,
    'scorecard': scorecard
  })

  return render_to_response('instructor.html', context)

def course(request):

  field_names = ['professor', 'course', 'instructor', 'difficulty']
  Row = namedtuple('Row', field_names)
  row1 = Row('Taskar', 3, 5, 4)
  row2 = Row('Marcus', 5, 2, 9)
  score_table = Table(field_names, [row1, row2], 12)

  number = 'CIS 520'
  title = 'Machine Learning'
  description = 'This course covers the foundations of machine learning.'
  course = Course(number, title, description)

  sb_course = ScoreBox('Course', 10)
  sb_instructor = ScoreBox('Instructor', 8)
  sb_difficulty = ScoreBox('Difficulty', 7)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row = ScoreBoxRow('Average', '80 sections', boxes)
  scorecard = ScoreCard([sb_row])

  context = RequestContext(request, {
    'course': course,
    'score_table': score_table,
    'scorecard': scorecard
  })
  return render_to_response('course.html', context)

def department(request):

  code = 'CIS'
  name = 'Computer and Information Science'

  field_names = ['Class', 'Course', 'Instructor', 'Difficulty']
  Row = namedtuple('Row', field_names)
  row1 = Row('CIS 110', 2.45, 2.55, 2.43)
  row2 = Row('CIS 120', 1.11, 2.34, 3.41)
  row3 = Row('CIS 121', 3.42, 1.12, 2.36)
  score_table = Table(field_names, [row1, row2, row3], 12)

  department = Department(code, name)

  context = {
    'department': department,
    'score_table': score_table
  } 

  return render_to_response('department.html', context)

def browse(request):
  return render_to_response('browse.html')

def faq(request):
  return render_to_response('FAQ.html')

def about(request):
  return render_to_response('about.html')
