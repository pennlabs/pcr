from __future__ import division
from collections import defaultdict, namedtuple
from itertools import groupby

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.scorecard_tag import ScoreCard, ScoreBoxRow, ScoreBox
from templatetags.table import Table

from helper import getSectionsTable, build_course, build_history, build_section
from api import pcr


RATING_STRINGS = ('Course', 'Instructor', 'Difficulty')
RATING_FIELDS = ('course', 'instructor', 'difficulty')


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


COURSE_OUTER = ('id', 'Professor') + RATING_STRINGS + ('sections',)
COURSE_OUTER_HIDDEN = ('id', 'professor') + RATING_FIELDS + ('sections',) 

COURSE_INNER = ('Semester',) + RATING_STRINGS
COURSE_INNER_HIDDEN =  ('semester',) + RATING_FIELDS

def course(request, course_id):
  raw_coursehistory = pcr('coursehistory', course_id)
  course = {
    'title': raw_coursehistory['name'],
    'subtitle': None,
    'description': None
  }
  
  #Get sections here
  #group by instructor
  instructors = defaultdict(list)
  instructor_id = {}
  for raw_course in raw_coursehistory["courses"]:
    semester = raw_course['semester']
    course_id = raw_course['id']
    raw_sections = pcr('course', course_id, "sections")['values']
    for raw_section in raw_sections:
      sectionnum = raw_section['sectionnum']
      raw_reviews = pcr('course', course_id, 'section', sectionnum, 'reviews')['values']
      raw_instructors = raw_section['instructors']

      #TODO Change this to not be static
      if raw_instructors is None:
        raw_instructors = [{'id': 1, 'name': 'Speigal'}]

      for raw_instructor, raw_review in zip(raw_instructors, raw_reviews):
        name = raw_instructor['name']
        instructor_id[name] = raw_instructor['id']
        raw_ratings = raw_review['ratings']
        review = dict([(attr, raw_ratings[attr]) for attr in RATING_STRINGS])
        review['Semester'] = semester
        instructors[name].append(review)

  table_body = []
  for instructor in instructors:
    sections = []
    isections = instructors[instructor]
    #average
    course_avg, instructor_avg, difficulty_avg = 0, 0, 0
    for section in isections:
      semester = section['Semester']
      rcourse = section['Course Quality']
      rinstructor = section['Instructor Quality']
      rdifficulty = section['Difficulty']
      course_avg += float(rcourse)
      instructor_avg += float(rinstructor)
      difficulty_avg += float(rdifficulty)
      sections.append((semester, rcourse, rinstructor, rdifficulty))
    course_avg /= len(sections)
    instructor_avg /= len(sections)
    difficulty_avg /= len(sections)
    #recent
    recent = isections[-1]
    course_rec = float(recent['Course Quality'])
    instructor_rec = float(recent['Instructor Quality'])
    difficulty_rec = float(recent['Difficulty'])
    sections_table = Table(COURSE_INNER, COURSE_INNER_HIDDEN, sections)
    table_body.append([instructor_id[instructor], instructor,
      (course_avg, course_rec),
      (instructor_avg, instructor_rec),
      (difficulty_avg, difficulty_rec),
      sections_table])

  score_table = Table(COURSE_OUTER, COURSE_OUTER_HIDDEN, table_body)

  #Average
  raw_reviews = pcr('coursehistory', course_id, 'reviews')['values']
  #unfortunately, I need to count since some reviews are blank
  course_quality, instructor_quality, difficulty = 0.0, 0.0, 0.0
  completed_reviews = 0
  for raw_review in raw_reviews:
    ratings = raw_review['ratings']
    try:
      course_quality += float(ratings["Course Quality"])
      instructor_quality += float(ratings["Instructor Quality"])
      try:
        difficulty += float(ratings["Difficulty"])
      except KeyError:
        #some forms don't actually have difficulty
        #check out coursehistory/1207 for example. Not sure what to do
        difficulty = -1
      completed_reviews += 1
    except KeyError:
      #some ratings are an empty dict
      #check out coursehistory/1200 for example.
      continue
  course_quality /= completed_reviews
  instructor_quality /= completed_reviews
  try:
    difficulty /= completed_reviews
  except:
    pass

  sb_course     = ScoreBox('Course', course_quality)
  sb_instructor = ScoreBox('Instructor', instructor_quality)
  sb_difficulty = ScoreBox('Difficulty', difficulty)
  boxes         = (sb_course, sb_instructor, sb_difficulty)
  average       = ScoreBoxRow('Average', '%s sections' % completed_reviews, boxes)

  #Recent
  recent_ratings = raw_reviews[-1]['ratings']
  r_course_quality = recent_ratings["Course Quality"]
  r_instructor_quality = recent_ratings["Instructor Quality"]
  try:
    r_difficulty = recent_ratings["Difficulty"]
  except:
    r_difficulty = -1
  r_semester = raw_coursehistory["courses"][-1]["semester"]

  sb_course     = ScoreBox('Course', r_course_quality)
  sb_instructor = ScoreBox('Instructor', r_instructor_quality)
  sb_difficulty = ScoreBox('Difficulty', r_difficulty)
  boxes         = [sb_course, sb_instructor, sb_difficulty]
  recent        = ScoreBoxRow('Recent', r_semester, boxes)

  scorecard     = ScoreCard([average, recent])

  context = RequestContext(request, {
    'course': course,
    'score_table': score_table,
    'scorecard': scorecard
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
        course_avg += float(ratings['Course Quality'])
        instructor_avg += float(ratings['Instructor Quality'])
        try:
          difficulty_avg += float(ratings['Difficulty'])
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
