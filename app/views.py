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

  field_names = ['id', 'Class', 'Course', 'Instructor', 'Difficulty', 'Sections']
  Row = namedtuple('Row', field_names)
  row1 = Row(1, 'CIS 110', 3.2, 3.5, 3.3, getSectionsTable())
  row2 = Row(2, 'CIS 120', 3.1, 2.6, 2.4, getSectionsTable())
  row3 = Row(3, 'CIS 121', 3.0, 2.4, 3.4, getSectionsTable())
  score_table = Table(field_names, [row1, row2, row3])
  
  sb_course = ScoreBox('Course', 3.05)
  sb_instructor = ScoreBox('Instructor', 2.8)
  sb_difficulty = ScoreBox('Difficulty', 3.2)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row1 = ScoreBoxRow('Average', '80 sections', boxes)
  sb_course = ScoreBox('Course', 2.4)
  sb_instructor = ScoreBox('Instructor', 3.3)
  sb_difficulty = ScoreBox('Difficulty', 3.5)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row2 = ScoreBoxRow('Recent', 'Fall 2008', boxes)
  scorecard = ScoreCard([sb_row1, sb_row2])

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
  score_table = Table(field_names, [row1, row2])

  number = 'CIS 520'
  title = 'Machine Learning'
  description = 'This course covers the foundations of machine learning.'
  course = Course(number, title, description)

  sb_course     = ScoreBox('Course', 3.0)
  sb_instructor = ScoreBox('Instructor', 2.8)
  sb_difficulty = ScoreBox('Difficulty', 3.2)
  boxes         = [sb_course, sb_instructor, sb_difficulty]
  sb_row1       = ScoreBoxRow('Average', '80 sections', boxes)
  sb_course     = ScoreBox('Course', 2.4)
  sb_instructor = ScoreBox('Instructor', 3.3)
  sb_difficulty = ScoreBox('Difficulty', 3.5)
  boxes         = [sb_course, sb_instructor, sb_difficulty]
  sb_row2       = ScoreBoxRow('Recent', 'Fall 2008', boxes)
  scorecard     = ScoreCard([sb_row1, sb_row2])

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
  score_table = Table(field_names, [row1, row2, row3])

  department = Department(code, name)

  context = {
    'department': department,
    'score_table': score_table
  } 

  return render_to_response('department.html', context)

def browse(request):
  return render_to_response('browse.html')

def faq(request):
  return render_to_response('faq.html')

def about(request):
  return render_to_response('about.html')

# Helper function to get sections table
def getSectionsTable():
  field_names = ['Semester', 'Section', 'Course', 'Instructor', 'Difficulty']
  Row = namedtuple('Row', field_names)
  row1 = Row('Fall 2010', '001', 3.0, 3.2, 2.4)  
  row2 = Row('Spring 2009', '001', 3.1, 2.5, 3.2)
  return Table(field_names, [row1, row2]) 
