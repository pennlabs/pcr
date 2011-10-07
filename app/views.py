from __future__ import division
from collections import defaultdict, namedtuple
from itertools import groupby

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.scorecard_tag import ScoreCard, ScoreBoxRow, ScoreBox
from templatetags.table import Table

from helper import getSectionsTable, build_course, build_history, build_section
from api import *


RATING_STRINGS = ('Course', 'Instructor', 'Difficulty')
RATING_FIELDS = ('course', 'instructor', 'difficulty')

RATING_API = ('rCourseQuality', 'rInstructorQuality', 'rDifficulty')

def index(request):
  return render_to_response('index.html')


def instructor(request, id):
  raw_instructor = pcr('instructor', id)
  instructor = {
    'name': raw_instructor['name'],
    'title': raw_instructor['title'],
    'address': raw_instructor['address'],
    'phone': raw_instructor['phone'],
    'email': raw_instructor['email'] 
  }

  #Don't forget about getSectionsTable()
  #row3 = Row(3, 'CIS 121', 3.0, 2.4, 3.4, getSectionsTable())
  
  #probably want to reimplement Table...
  score_table = Table(COURSE, map(build_course, raw_instructor['courses']))
  
  sb_course = ScoreBox('Course', 3.05)
  sb_instructor = ScoreBox('Instructor', 2.8)
  sb_difficulty = ScoreBox('rDifficulty', 3.2)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row1 = ScoreBoxRow('Average', '80 sections', boxes)

  sb_course = ScoreBox('Course', 2.4)
  sb_instructor = ScoreBox('Instructor', 3.3)
  sb_difficulty = ScoreBox('rDifficulty', 3.5)
  boxes = [sb_course, sb_instructor, sb_difficulty]
  sb_row2 = ScoreBoxRow('Recent', 'Fall 2008', boxes)

  scorecard = ScoreCard([sb_row1, sb_row2])

  context = RequestContext(request, {
    'instructor': instructor,
    'score_table': score_table,
    'scorecard': scorecard
  })

  return render_to_response('instructor.html', context)


COURSE_OUTER = ('id', 'Professor') + RATING_STRINGS + ('sections',)
COURSE_OUTER_HIDDEN = ('id', 'professor') + RATING_FIELDS + ('sections',) 

COURSE_INNER = ('Semester',) + RATING_STRINGS
COURSE_INNER_HIDDEN =  ('semester',) + RATING_FIELDS

def course(request, coursehistory_id):
  coursehistory = CourseHistory(pcr('coursehistory', coursehistory_id))

  scorecard = [
      ScoreBoxRow('Average',
        '%s sections' % len(coursehistory.sections),
        [ScoreBox(display, coursehistory.average(attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)]),
      ScoreBoxRow('Recent',
        coursehistory.most_recent.semester,
        [ScoreBox(display, coursehistory.recent(attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)])]

  score_table = Table(COURSE_OUTER, COURSE_OUTER_HIDDEN,
      [[row_id, instructor.name] +
      #instructor averages
      [(instructor.average(rating),
        instructor.recent(rating))
        for rating in RATING_API] +
      #hack last cell (scores for each section)
      [Table(COURSE_INNER, COURSE_INNER_HIDDEN,
        [[section.semester] + [section.average(rating) for rating in RATING_API] for section in instructor.sections]
        )]
  for row_id, instructor in enumerate(coursehistory.instructors)])


  context = RequestContext(request, {
    'course': coursehistory,
    'scorecard': scorecard,
    'score_table': score_table
  })
  return render_to_response('course.html', context)

DEPARTMENT_OUTER = ('id', 'Course',) + RATING_STRINGS + ('courses',)
DEPARTMENT_OUTER_HIDDEN = ('id', 'course',) + RATING_FIELDS + ('courses',)

def department(request, id):
  raw_depts = pcr('depts')['values']

  #hacky solution to get department name
  for raw_dept in raw_depts:
    if raw_dept['id'] == id:
      name = raw_dept['name']
      break

  department = {
      'code': id,
      'name': name
    }

  table_body = []
  raw_histories = pcr('dept', id)['histories']
  for raw_history in raw_histories:
    history_id = raw_history['id']
    course_name = raw_history['name']
    raw_reviews = pcr('coursehistory', history_id, 'reviews')['values']
    course_avg, instructor_avg, difficulty_avg = 0, 0, 0
    for raw_review in raw_reviews:
      ratings = raw_review['ratings']
      if ratings:
        course_avg += float(ratings['rCourseQuality'])
        instructor_avg += float(ratings['rInstructorQuality'])
        try:
          difficulty_avg += float(ratings['rDifficulty'])
        except:
          pass
    if raw_reviews:
      course_avg /= len(raw_reviews)
      instructor_avg /= len(raw_reviews)
      difficulty_avg /= len(raw_reviews)
    table_body.append((history_id, course_name, course_avg, instructor_avg, difficulty_avg, ""))
  score_table = Table(DEPARTMENT_OUTER, DEPARTMENT_OUTER_HIDDEN, table_body)

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
