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


class ScoreCard(object):
  '''Build a scorecard for the given sections.'''
  def __init__(self, sr_pairs):
    self.sr_pairs = [pair for pair in sr_pairs]

  @property
  def average(self):
    sections, reviews = zip(*self.sr_pairs)
    return ScoreBoxRow('Average', '%s sections' % len(sections),
        [ScoreBox(display, average(reviews, attr))
          for display, attr in SCORECARD]
        )

  @property
  def recent(self):
    most_recent, most_recent_review = max(self.sr_pairs, key=by_semester)
    return ScoreBoxRow('Recent', most_recent.semester,
        [ScoreBox(display, getattr(most_recent_review, attr))
          for display, attr in SCORECARD]
        )

  def __iter__(self):
    yield self.average
    yield self.recent


ScoreBox = namedtuple('ScoreBox', ['description', 'number'])


class ScoreBoxRow(list):
  def __init__(self, title, subtitle, boxes):
    super(ScoreBoxRow, self).__init__(boxes)
    self.title = title
    self.subtitle = subtitle


@tag(register, [])
def scorecard_widget(context):
  '''Create a scorecard.'''
  return render_to_string('templates/scorecard/scorecard.html', context)
