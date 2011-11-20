from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.parser import Variable, Optional, Constant, Name
from templatetag_sugar.register import tag

register = template.Library()


by_semester = lambda sr_pair: sr_pair[0].semester


class Table(object):
  def __init__(self, head, body):
    self.head = head
    self.body = body


def parse_attr(review, attr):
  """Try to parse an attribute from a review.
  In the case an attribute cannot be parsed, returns ERROR."""
  try:
    val = getattr(review, attr)
  except AttributeError:
    return None


class ScoreTable(Table):
  def __init__(review_tree, key_map, key_columns, key_fields):
    columns = get_columns(review for _, review in chain(*review_tree.values()))

    body = []
    for row_id, key in enumerate(sorted(review_tree)):
      sr_pairs = review_tree[key]
      sections, reviews = zip(*sr_pairs)
      section_table = build_section_table(key, review_tree, strings, fields, columns)
      #append row 
      sr_pairs.sort(key=lambda pair: pair[0].semester, reverse=False)
      most_recent, most_recent_review = sr_pairs[-1]
      body.append(
          [row_id]        + key_map(key)
          + [(average(reviews, column), parse_attr(most_recent_review, column)) for column in columns]        + [section_table])
    return Table(
        key_columns + strings + ('sections',),      key_fields + fields + ('sections',),
        body
        )   


def get_attributes(self, reviews):
  '''Filter attributes to include only relevant data.
  In the case that a course form changes over time, get the union of all attributes.'''
  for attribute in ATTRIBUTES:
    for review in reviews:
      try:
        yield getattr(reivew, attribute)
        break
      except AttributeError:
        continue


class SectionTable(Table):
  default_head = ('Semester', 'Name', 'Section', 'Responses')

  def __init__(key, review_tree, columns):
    self.head = self.default_head + columns
    self.body = []
    for section, review in sorted(review_tree[key], key=by_semester, reverse=True):
      self.body.append(
          [section.semester, section.name, section.sectionnum, "%s/%s" % (review.num_reviewers, review.num_students)]
          + parse_review(review, columns)
          )
      self.comments = review.comments


@tag(register, [Variable()])
def course_table(context, coursehistory):
  '''Create a table.'''
  head = ['id', 'link', 'Instructor', 'Name']
  body = []
  for course in coursehistory.courses:
    for section in course.sections:
      for instructor in section.instructors:
        body.append(['id', 'link', instructor.name])
  new_context = {
    'table': Table(head, body)
  }
  return render_to_string('templatetags/course_table.html', new_context)


@tag(register, [Variable()])
def instructor_table(context, table):
  '''Create a table.'''
  new_context = {
    'table': table
  }
  return render_to_string('templatetags/instructor_table.html', new_context)


@tag(register, [Variable(), Variable()])
def section_table(context, table, row_id):
  '''Create a table.'''
  new_context = {
    'table': table,
    'row_id': row_id
  }
  return render_to_string('templatetags/section_table.html', new_context)
