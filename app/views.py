from __future__ import division
from collections import defaultdict, namedtuple
import json
from itertools import groupby

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.prettify import PRETTIFY_REVIEWBITS, ORDER, PRETTIFY_SEMESTER
from templatetags.scorecard_tag import ScoreBoxRow, ScoreBox
from templatetags.table import Table

from api import pcr
from average import average, ERROR
from wrapper import Instructor, CourseHistory


RATING_API = ORDER
RATING_STRINGS = tuple([PRETTIFY_REVIEWBITS[v] for v in ORDER])
RATING_FIELDS = tuple(["".join(words.split()) for words in ORDER])

SCORECARD_STRINGS = ('Course', 'Instructor', 'Difficulty')
SCORECARD_FIELDS = ('course', 'instructor', 'difficulty') 
SCORECARD_API = ('rCourseQuality', 'rInstructorQuality', 'rDifficulty')

INSTRUCTOR_OUTER = ('id', 'link', 'Code', 'Name')
INSTRUCTOR_OUTER_HIDDEN = ('id', 'link', 'code', 'name')

COURSE_OUTER = ('id', 'link', 'Instructor')
COURSE_OUTER_HIDDEN = ('id', 'link', 'instructor')

TABLE_INNER = ('Semester', 'Section')
TABLE_INNER_HIDDEN =  ('semester', 'section')

#UNUSED
DEPARTMENT_OUTER = ('id', 'Course',) + RATING_STRINGS + ('courses',)
DEPARTMENT_OUTER_HIDDEN = ('id', 'course',) + RATING_FIELDS + ('courses',)


def index(request):
  return render_to_response('index.html')

def json_response(result_dict):
  return HttpResponse(content=json.dumps(result_dict))


def prettify_semester(semester):
  return "%s %s" % (PRETTIFY_SEMESTER[semester[-1]], semester[:-1])

def parse_attr(review, attr):
  try:
    val = getattr(review, attr)
  except:
    return ERROR
  else:
    return val

def parse_review(review, attrs):
  return [parse_attr(review, attr) for attr in attrs]  


def build_scorecard(review_tree):
  '''Build a scorecard for the given sections.'''
  sr_pairs = sum(review_tree.values(), [])

  #average
  sections, reviews = zip(*sr_pairs)
  avg = ScoreBoxRow('Average', '%s sections' % len(sections),
      [ScoreBox(display, average(reviews, attr))
        for display, attr in zip(SCORECARD_STRINGS, SCORECARD_API)])

  #recent
  for section, review in sorted(sr_pairs, key=lambda sr_pair: sr_pair[0].semester, reverse=True):
    if review.raw != dict():
      most_recent, most_recent_review = section, review
      break
  if most_recent is None:
    return (avg,)
  else:
    parsed = parse_review(most_recent_review, SCORECARD_API)
    boxes = [ScoreBox(display, attr) for display, attr in zip(SCORECARD_STRINGS, parsed)]
    recent = ScoreBoxRow('Recent', prettify_semester(most_recent.semester), boxes)
  return avg, recent


def get_relevant_columns(review_tree):
  '''Filter columns to include only relevant data.
  In the case that a course form changes over time, get the union of all columns.'''
  sections, reviews = zip(*sum(review_tree.values(), []))
  strings, fields, columns = tuple(), tuple(), tuple()
  for string, field, column in zip(RATING_STRINGS, RATING_FIELDS, RATING_API):
    for review in reviews:
      if hasattr(review, column):
        strings += (string,)
        fields += (field,)
        columns += (column,)
        break
  return strings, fields, columns


def build_section_table(key, review_tree, strings, fields, columns):
  section_body = []
  for section, review in sorted(review_tree[key], key=lambda sr_pair: sr_pair[0].semester, reverse=True):
    section_body.append(
        [prettify_semester(section.semester), section.sectionnum] 
        + parse_review(review, columns)
        + [review.comments]
        + ["%s/%s" % (review.num_reviewers, review.num_students)]
        )
  return Table(TABLE_INNER + strings + ('Returned', 'comments',), TABLE_INNER_HIDDEN + fields + ('reviewers', 'comments',), section_body)


def build_score_table(review_tree, key_map, key_columns, key_fields):
  strings, fields, columns = get_relevant_columns(review_tree)
  
  body = []
  for row_id, key in enumerate(sorted(review_tree)):
    sr_pairs = review_tree[key]
    sections, reviews = zip(*sr_pairs)
    section_table = build_section_table(key, review_tree, strings, fields, columns)

    #append row
    sr_pairs.sort(key=lambda pair: pair[0].semester, reverse=True)
    most_recent, most_recent_review = sr_pairs[-1]
    body.append(
        [row_id]
        + key_map(key)
        + [(average(reviews, column), parse_attr(most_recent_review, column)) for column in columns]
        + [section_table])

  return Table(
      key_columns + strings + ('sections',),
      key_fields + fields + ('sections',),
      body
      )

def instructor(request, id):
  instructor = Instructor(pcr('instructor', id))

  review_tree = defaultdict(list)
  for section in instructor.sections:
    coursehistory = section.course.coursehistory
    for review in section.reviews:
      review_tree[coursehistory].append((section, review))


  def key_map(key):
    return ['course/%s' % "-".join(key.subtitle.split()), key.subtitle, key.name]

  scorecard = build_scorecard(review_tree)
  score_table = build_score_table(review_tree, key_map, INSTRUCTOR_OUTER, INSTRUCTOR_OUTER_HIDDEN)

  context = RequestContext(request, {
    'instructor': instructor,
    'scorecard': scorecard,
    'score_table': score_table,
    'base_dir': '../'
  })

  return render_to_response('instructor.html', context)


def course(request, dept, id):
  dept = dept.upper()
  title = '%s-%s' % (dept, id)
  coursehistory = CourseHistory(pcr('coursehistory', title))

  review_tree = defaultdict(list)
  for course in coursehistory.courses:
    if not hasattr(coursehistory, 'description') and course.description:
      coursehistory.description = course.description
    for section in course.sections:
      for review in section.reviews:
        review_tree[review.instructor].append((section, review))

  def key_map(instructor):
    return ['instructor/%s' % instructor.id, instructor.name]

  scorecard = build_scorecard(review_tree)
  score_table = build_score_table(review_tree, key_map, COURSE_OUTER,COURSE_OUTER_HIDDEN)

  aliases = coursehistory.aliases
  aliases.remove(title)
  context = RequestContext(request, {
    'aliases': aliases,
    'title': "%s %s" % (dept, id),
    'course': coursehistory,
    'scorecard': scorecard,
    'score_table': score_table,
    'base_dir': '../'
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
  def alias_to_code(alias, sep="-"):
    code, num = alias.split('-')
    return "%s%s%03d" % (code, sep, int(num))
  courses_from_api = pcr('coursehistories')['values']
  courses = [{"category": "Courses",
              "title": alias_to_code(course['aliases'][0], ' '),
              "desc": course['name'],
              "url": "course/" + alias_to_code(course['aliases'][0]),
              "keywords": " ".join([alias_to_code(alias.lower(), sep) \
                            for sep in ['', '-', ' '] for alias in course['aliases']] \
                        + [course['name'].lower()])
             } for course in courses_from_api if len(course['aliases']) > 0]
  

  #2. Hit API up for instructor data, push into nop's desired format
  instructors_from_api = pcr('instructors')['values']  
  instructors=[{"category": "Instructors",
                "title": instructor['name'],
                "desc": ", ".join(instructor['departments']),
                "url": "instructor/" + instructor['id'],
                "keywords": instructor['name'].lower()
               } for instructor in instructors_from_api 
                 if 'departments' in instructor]

  #3. Respond in JSON
  return json_response({"courses":courses, "instructors":instructors})

def browse(request):
  context = {
    'base_dir': "../"
  } 
  return render_to_response('browse.html', context)

def faq(request):
  context = {
    'base_dir': "../"
  } 
  return render_to_response('faq.html', context)

def about(request):
  context = {
    'base_dir': "../"
  } 
  return render_to_response('about.html', context)
