from collections import namedtuple

from django import template
from django.template import RequestContext
from django.template.loader import render_to_string

from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

from average import average


register = template.Library()

SCORECARD = ( 
  ('Course', 'rCourseQuality'),
  ('Instructor','rInstructorQuality'),
  ('Difficulty', 'rDifficulty')
  )

by_semester = lambda sr_pair: sr_pair[0].semester


Cell = namedtuple('Cell', ['description', 'number'])


class Row(list):
  def __init__(self, title, subtitle, cells):
    super(Row, self).__init__(cells)
    self.title = title
    self.subtitle = subtitle


class ScoreCard(object):
  '''Build a scorecard for the given sections.'''
  def __init__(self, sr_pairs):
    self.sr_pairs = [pair for pair in sr_pairs]

  @property
  def average(self):
    sections, reviews = zip(*self.sr_pairs)
    return Row('Average', '%s sections' % len(sections),
        [Cell(desc, average(reviews, attr)) for desc, attr in SCORECARD]
        )

  @property
  def recent(self):
    most_recent, most_recent_review = max(self.sr_pairs, key=by_semester)
    return Row('Recent', most_recent.semester,
        [Cell(desc, getattr(most_recent_review, attr)) for desc, attr in SCORECARD]
        )

  def __iter__(self):
    yield self.average
    yield self.recent


@tag(register, [Variable()])
def scorecard(context, item):
  '''Create a scorecard.'''
  new_context = {
    'scorecard': None
    }
  return render_to_string('templatetags/scorecard.html', new_context)
