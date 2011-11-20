from __future__ import division
from collections import namedtuple

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from apps.app.models import CourseHistory, Instructor, Review


register = template.Library()

SCORECARD = ( 
  ('Course', 'rCourseQuality'),
  ('Instructor','rInstructorQuality'),
  ('Difficulty', 'rDifficulty')
  )

average = lambda values: sum(values) / len(values)
by_semester = lambda sr_pair: sr_pair[0].course.semester


Cell = namedtuple('Cell', ['description', 'number'])


class Row(list):
  def __init__(self, title, subtitle, cells):
    super(Row, self).__init__(cells)
    self.title = title
    self.subtitle = subtitle


class ScoreCard(list):
  '''Build a scorecard for the given sections.'''
  def __init__(self, sr_pairs):
    sections, reviews = zip(*sr_pairs)

    averaged = Row('Average', '%s sections' % len(sections),
        [Cell(desc, average([review.ratings[attr] for review in reviews]))
          for desc, attr in SCORECARD]
        )

    most_recent, most_recent_review = max(sr_pairs, key=by_semester)
    recent = Row('Recent', most_recent.course.semester,
        [Cell(desc, most_recent_review.ratings[attr]) for desc, attr in SCORECARD]
        )

    super(ScoreCard, self).__init__([averaged, recent])


@tag(register, [Variable()])
def scorecard(context, item):
  '''Create a scorecard.'''
  sr_pairs = []
  if type(item) == CourseHistory:
    for course in item.courses:
      for section in course.sections:
        for instructor in section.instructors:
          sr_pairs.append((section, Review(section.id, instructor.id)))
  new_context = {
    'scorecard': ScoreCard(sr_pairs)
    }
  return render_to_string('templatetags/scorecard.html', new_context)
