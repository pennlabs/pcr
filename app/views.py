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

#TODO: Get this and filter stuff out
CURRENT_SEMESTER = None

RATING_STRINGS = ('Course', 'Instructor', 'Difficulty')
RATING_FIELDS = ('course', 'instructor', 'difficulty')

RATING_API = ('rCourseQuality', 'rInstructorQuality', 'rDifficulty')

def index(request):
  return render_to_response('index.html')

INSTRUCTOR_OUTER = ('id', 'Course') + RATING_STRINGS + ('sections',)
INSTRUCTOR_OUTER_HIDDEN = ('id', 'course') + RATING_FIELDS + ('sections',) 

INSTRUCTOR_INNER = ('Semester',) + RATING_STRINGS
INSTRUCTOR_INNER_HIDDEN =  ('semester',) + RATING_FIELDS

def instructor(request, id):
  instructor = Instructor(pcr('instructor', id))
  sections = instructor.sections
  coursehistories = defaultdict(list)
  for section in sections:
    coursehistories[section.course.coursehistory.name].append(section)

  scorecard = [
      ScoreBoxRow('Average',
        '%s sections' % len(instructor.sections),
        [ScoreBox(display, average([review for section in instructor.sections for review in section.reviews], attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)]),
      ScoreBoxRow('Recent',
        instructor.most_recent.semester,
        [ScoreBox(display, average([review for review in instructor.sections[-1].reviews], attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)])]
  
  #create a map from coursehistory to sections taught by professor
  #use average of the sections to create averages / recent
  score_table = Table(INSTRUCTOR_OUTER, INSTRUCTOR_OUTER_HIDDEN,
      [[row_id, coursehistory] +

      [(average([review for section in coursehistories[coursehistory] for review in section.reviews], rating),
        recent([review for section in coursehistories[coursehistory] for review in section.reviews], rating))
        for rating in RATING_API] +

      [Table(INSTRUCTOR_INNER, INSTRUCTOR_INNER_HIDDEN,
        [[section.semester] + [average(section.reviews, rating) for rating in RATING_API] for section in coursehistories[coursehistory]]
        )]
  for row_id, coursehistory in enumerate(coursehistories)])

  context = RequestContext(request, {
    'instructor': instructor,
    'scorecard': scorecard,
    'score_table': score_table
  })

  return render_to_response('instructor.html', context)


COURSE_OUTER = ('id', 'Professor') + RATING_STRINGS + ('sections',)
COURSE_OUTER_HIDDEN = ('id', 'professor') + RATING_FIELDS + ('sections',) 

COURSE_INNER = ('Semester', 'Section') + RATING_STRINGS
COURSE_INNER_HIDDEN =  ('semester', 'section') + RATING_FIELDS

def course(request, dept, id):
  coursehistory = CourseHistory(pcr('coursehistory', '%s-%s' % (dept, id)))

  scorecard = [
      ScoreBoxRow('Average',
        '%s sections' % len([section for section in coursehistory.sections if section.course.coursehistory == coursehistory]),
        [ScoreBox(display, average([review for course in coursehistory.courses for section in course.sections if section.course.coursehistory == coursehistory for review in section.reviews], attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)]),
      ScoreBoxRow('Recent',
        coursehistory.most_recent.semester,
        [ScoreBox(display, recent([review for course in coursehistory.courses for section in course.sections if section.course.coursehistory == coursehistory for review in section.reviews], attr))
          for display, attr in zip(RATING_STRINGS, RATING_API)])]

  score_table = Table(COURSE_OUTER, COURSE_OUTER_HIDDEN,
      [[row_id, instructor.name] +
      #instructor averages
      [(average([review for section in instructor.sections if section.course.coursehistory == coursehistory for review in section.reviews], rating),
        recent([review for section in instructor.sections if section.course.coursehistory == coursehistory for review in section.reviews], rating))
        for rating in RATING_API] +
      #hack last cell (scores for each section)
      [Table(COURSE_INNER, COURSE_INNER_HIDDEN,
        [[section.semester, section.sectionnum] + [average(section.reviews, rating) for rating in RATING_API] for section in instructor.sections if section.course.coursehistory == coursehistory]
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
