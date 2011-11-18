from __future__ import division
from collections import defaultdict
import json

from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import Context, loader, RequestContext

from templatetags.prettify import PRETTIFY_REVIEWBITS, ORDER, PRETTIFY_SEMESTER
from templatetags.scorecard_tag import ScoreBoxRow, ScoreBox
from templatetags.table import Table

from average import average, ERROR
from models import Instructor, CourseHistory


RATING_API = ORDER
RATING_STRINGS = tuple(PRETTIFY_REVIEWBITS[v] for v in ORDER)
RATING_FIELDS = tuple("".join(words.split()) for words in ORDER)


def index(request):
  return render_to_response('index.html')


def json_response(result_dict):
  return HttpResponse(content=json.dumps(result_dict))


def prettify_semester(semester):
  return "%s %s" % (PRETTIFY_SEMESTER[semester[-1]], semester[:-1])


def parse_attr(review, attr):
  """Try to parse an attribute from a review.
  In the case an attribute cannot be parsed, returns ERROR."""
  try:
    val = getattr(review, attr)
  except:
    return ERROR
  else:
    return "%.2f" % val


def parse_review(review, attrs):
  """Parse all of the attributes from a review."""
  return [parse_attr(review, attr) for attr in attrs]  


SCORECARD_STRINGS = ('Course', 'Instructor', 'Difficulty')
SCORECARD_FIELDS = ('course', 'instructor', 'difficulty') 
SCORECARD_API = ('rCourseQuality', 'rInstructorQuality', 'rDifficulty')
def build_scorecard(review_tree):
  '''Build a scorecard for the given sections.'''
  sr_pairs = sum(review_tree.values(), [])
  if len(sr_pairs) == 0:
    raise ValueError("No reviews found")

  #average
  sections, reviews = zip(*sr_pairs)
  avg = ScoreBoxRow('Average', '%s sections' % len(sections),
      [ScoreBox(display, average(reviews, attr))
        for display, attr in zip(SCORECARD_STRINGS, SCORECARD_API)])

  #recent
  for section, review in sorted(sr_pairs, key=lambda sr_pair: sr_pair[0].semester, reverse=True):
    if review._raw != dict():
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
  for string, field, column in zip(RATING_STRINGS, RATING_FIELDS, RATING_API):
    for review in reviews:
      if hasattr(review, column):
        yield (string, field, column)
        break


def format_comments(comment):
  return (comment or "").replace("\n", "<br />")


TABLE_INNER = ('Semester', 'Name', 'Section', 'Responses')
TABLE_INNER_HIDDEN =  ('semester', 'name', 'section', 'responses') # not sure of difference?
def build_section_table(key, review_tree, strings, fields, columns):
  section_body = []

  for section, review in sorted(review_tree[key], key=lambda sr_pair: sr_pair[0].semester, reverse=True):
    section_body.append(
        [prettify_semester(section.semester), section.name, section.sectionnum, "%s/%s" % (review.num_reviewers, review.num_students)]
        + parse_review(review, columns)
        + [format_comments(review.comments)] 
        )
  return Table(TABLE_INNER + strings + ('comments',), TABLE_INNER_HIDDEN + fields + ('comments',), section_body)


def build_score_table(review_tree, key_map, key_columns, key_fields):
  try:
    strings, fields, columns = zip(*get_relevant_columns(review_tree))
  except ValueError:
    raise ValueError("No review bits found.")

  body = []
  for row_id, key in enumerate(sorted(review_tree)):
    sr_pairs = review_tree[key]
    sections, reviews = zip(*sr_pairs)
    section_table = build_section_table(key, review_tree, strings, fields, columns)

    #append row 
    sr_pairs.sort(key=lambda pair: pair[0].semester, reverse=False)
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


INSTRUCTOR_OUTER = ('id', 'link', 'Code', 'Name')
INSTRUCTOR_OUTER_HIDDEN = ('id', 'link', 'code', 'name')
def instructor(request, id):
  instructor = Instructor(id)

  review_tree = defaultdict(list) #coursehistory => list((section, review))
  for section in instructor.sections:
    coursehistory = section.course.coursehistory
    for review in section.reviews:
      if review.instructor == instructor:
        review_tree[coursehistory].append((section, review))

  def key_map(key):
    # returns [link, course code, name]
    sections = [sr[0] for sr in review_tree[key]]
    names = set([section.name for section in sections])
    name = names.pop() if len(names) == 1 else 'Various'
    return ['course/%s' % "-".join(key.code.split()), key.code, name]
  try:
    try:
      scorecard = build_scorecard(review_tree)
    except ValueError as e:
      raise e
    try:
      score_table = build_score_table(review_tree, key_map, INSTRUCTOR_OUTER, INSTRUCTOR_OUTER_HIDDEN)
    except ValueError as e:
      raise e
  except ValueError:
    context = RequestContext(request, {
      'instructor': instructor,
      'error': True,
      'base_dir': '../'
    })
    return render_to_response('instructor-error.html', context)
  else:
    context = RequestContext(request, {
      'instructor': instructor,
      'scorecard': scorecard,
      'score_table': score_table,
      'base_dir': '../'
    })
    return render_to_response('instructor.html', context)


COURSE_OUTER = ('id', 'link', 'Instructor', 'Name')
COURSE_OUTER_HIDDEN = ('id', 'link', 'instructor', 'name')
def course(request, dept, id):
  dept = dept.upper()
  title = '%s-%s' % (dept, id)
  coursehistory = CourseHistory(title)

  review_tree = defaultdict(list)
  for course in coursehistory.courses:
    for section in course.sections:
      for review in section.reviews:
        review_tree[review.instructor].append((section, review))

  aliases = coursehistory.aliases - set([title])

  def key_map(instructor):
    sections = [sr[0] for sr in review_tree[instructor]]
    names = set([section.name for section in sections])
    name = names.pop() if len(names) == 1 else 'Various'
    return ['instructor/%s' % instructor.id, instructor.name, name]

  try:
    try:
      scorecard = build_scorecard(review_tree)
    except ValueError as e:
      raise e
    try:
      score_table = build_score_table(review_tree, key_map, COURSE_OUTER, COURSE_OUTER_HIDDEN)
    except ValueError as e:
      raise e
  except ValueError:
    context = RequestContext(request, {
      'aliases': aliases,
      'title': "%s %s" % (dept, id),
      'course': coursehistory,
      'error': True,
      'base_dir': '../'
    })
    return render_to_response('course-error.html', context)
  else:
    context = RequestContext(request, {
      'aliases': aliases,
      'title': "%s %s" % (dept, id),
      'course': coursehistory,
      'scorecard': scorecard,
      'score_table': score_table,
      'base_dir': '../'
    })
    return render_to_response('course.html', context)


def autocomplete_data(request):
  #1. Hit API up for course-history data, push into nop's desired format
  def alias_to_code(alias, sep="-"):
    code, num = alias.split('-')
    return "%s%s%03d" % (code, sep, int(num))
  courses_from_api = api('coursehistories')['values']
  courses = [{"category": "Courses",
              "title": alias_to_code(alias, ' '),
              "desc": course['name'],
              "url": "course/" + alias_to_code(alias),
              "keywords": " ".join([alias_to_code(alias.lower(), sep) \
                            for sep in ['', '-', ' ']] \
                        + [course['name'].lower()])
             } for course in courses_from_api 
               for alias in course['aliases']]

  #2. Hit API up for instructor data, push into nop's desired format
  instructors_from_api = api('instructors')['values']  
  instructors=[{"category": "Instructors",
                "title": instructor['name'],
                "desc": ", ".join(instructor['departments']),
                "url": "instructor/" + instructor['id'],
                "keywords": instructor['name'].lower()
               } for instructor in instructors_from_api 
                 if 'departments' in instructor]

  #3. Respond in JSON
  return json_response({"courses":courses, "instructors":instructors})


def static(request, page):
  context = {
    'base_dir': "../",
    'content': api('apisite-static', page)
  }
  return render_to_response('static.html', context)
