from __future__ import division
from collections import defaultdict, namedtuple
import json
from itertools import groupby

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.scorecard_tag import ScoreCard, ScoreBoxRow, ScoreBox
from templatetags.table import Table

from api import *
from helper import getSectionsTable, build_course, build_history, build_section
from templatetags.prettify import PRETTIFY_REVIEWBITS

#TODO: Get this and filter stuff out
CURRENT_SEMESTER = None

RATING_STRINGS = tuple(PRETTIFY_REVIEWBITS.values())
RATING_FIELDS = tuple(["".join(words.split()) for words in PRETTIFY_REVIEWBITS.values()])
RATING_API = tuple(PRETTIFY_REVIEWBITS.keys())

SCORECARD_STRINGS = ('Course', 'Instructor', 'Difficulty')
SCORECARD_FIELDS = ('course', 'instructor', 'difficulty') 
SCORECARD_API = ('rCourseQuality', 'rInstructorQuality', 'rDifficulty')

def json_response(result_dict):
  return HttpResponse(content=json.dumps(result_dict))

INSTRUCTOR_OUTER = ('id', 'Course') + RATING_STRINGS + ('sections',)
INSTRUCTOR_OUTER_HIDDEN = ('id', 'course') + RATING_FIELDS + ('sections',) 

INSTRUCTOR_INNER = ('Semester',) + RATING_STRINGS
INSTRUCTOR_INNER_HIDDEN =  ('semester',) + RATING_FIELDS

COURSE_OUTER = ('id', 'Professor') + RATING_STRINGS + ('sections',)
COURSE_OUTER_HIDDEN = ('id', 'professor') + RATING_FIELDS + ('sections',) 

COURSE_INNER = ('Semester', 'Section') + RATING_STRINGS
COURSE_INNER_HIDDEN =  ('semester', 'section') + RATING_FIELDS

DEPARTMENT_OUTER = ('id', 'Course',) + RATING_STRINGS + ('courses',)
DEPARTMENT_OUTER_HIDDEN = ('id', 'course',) + RATING_FIELDS + ('courses',)


def build_scorecard(sections):
  '''Build a scorecard for the given sections.'''
  avg = ScoreBoxRow('Average', '%s sections' % len(sections),
      [ScoreBox(display, average([review for section in sections for review in section.reviews], attr))
        for display, attr in zip(SCORECARD_STRINGS, SCORECARD_API)])
  most_recent = sections[-1]
  recent = ScoreBoxRow('Recent', most_recent.semester,
      [ScoreBox(display, average([review for review in most_recent.reviews], attr))
        for display, attr in zip(SCORECARD_STRINGS, SCORECARD_API)])
  return (avg, recent)


def index(request):
  return render_to_response('index.html')


def instructor(request, id):
  instructor = Instructor(pcr('instructor', id))
  sections = instructor.sections
  coursehistories = defaultdict(list)
  for section in sections:
    coursehistories[section.course.coursehistory.name].append(section)

  scorecard = build_scorecard(sections)
  
  #create a map from coursehistory to sections taught by professor
  #use average of the sections to create averages / recent
  body = []
  for row_id, coursehistory in enumerate(coursehistories):
    section_reviews = section.reviews
    reviews = [review for section in coursehistories[coursehistory] for review in section_reviews]

    #build subtable
    section_body = []
    for section in coursehistories[coursehistory]:
      section_body.append(
          [section.semester] + [average(section_reviews, rating) for rating in RATING_API]
          )
    section_table = Table(INSTRUCTOR_INNER, INSTRUCTOR_INNER_HIDDEN, section_body)

    #append row
    body.append(
        [row_id, coursehistory] +

        [(average(reviews, rating), recent(reviews, rating)) for rating in RATING_API] +

        [section_table]
      )

  score_table = Table(INSTRUCTOR_OUTER, INSTRUCTOR_OUTER_HIDDEN, body)

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
  sections = [section for section in coursehistory.sections if section.course.coursehistory == coursehistory]

  scorecard = build_scorecard(sections)

  body = []
  for row_id, instructor in enumerate(coursehistory.instructors):
    reviews = [review for section in instructor.sections if section.course.coursehistory == coursehistory for review in section.reviews]

    #build subtable
    section_body = []
    for section in instructor.sections:
      if section.course.coursehistory == coursehistory:
        section_body.append(
            [section.semester, section.sectionnum] + [average(section.reviews, rating) for rating in RATING_API]
            )
    section_table = Table(COURSE_INNER, COURSE_INNER_HIDDEN, section_body)

    #append row
    body.append(
        [row_id, instructor.name] +

        [(average(reviews, rating), recent(reviews, rating)) for rating in RATING_API] +

        [section_table]
      )

  score_table = Table(COURSE_OUTER, COURSE_OUTER_HIDDEN, body)

  context = RequestContext(request, {
    'course': coursehistory,
    'scorecard': scorecard,
    'score_table': score_table
  })
  return render_to_response('course.html', context)


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

def autocomplete_data(request):
  #1. Hit API up for course-history data, push into nop's desired format
  courses_from_api = pcr('coursehistories')['values']
  courses = [{"category": "Courses",
              "title": course['aliases'][0],
              "desc": course['name'],
              "url": "course/%s-%s" % tuple(course['aliases'][0].split(" ")),
              "keywords": " ".join([sep.join(alias.lower().split(" ")) \
                            for sep in ['', '-', ' '] for alias in course['aliases']] \
                        + [course['name'].lower()])
             } for course in courses_from_api if len(course['aliases']) > 0]
  #TODO - econ 1 = econ 001 (in terms of aliases)

  #2. Hit API up for instructor data, push into nop's desired format
  instructors_from_api = pcr('instructors')['values']  
  instructors=[{"category": "Instructors",
                "title": instructor['name'],
                "desc": "teaches " + ", ".join(instructor['departments']),
                "url": "instructor/" + instructor['id'],
                "keywords": instructor['name'].lower()
               } for instructor in instructors_from_api 
                 if 'departments' in instructor]

  #3. Respond in JSON
  return json_response({"courses":courses, "instructors":instructors})

def browse(request):
  return render_to_response('browse.html')

def faq(request):
  return render_to_response('faq.html')

def about(request):
  return render_to_response('about.html')
