from __future__ import division

import urllib
import urllib2
import json
from collections import defaultdict

API = "http://pennapps.com/courses-ceasarb/"
TOKEN = "pennappsdemo"

def pcr(*args, **kwargs):
  kwargs["token"] = TOKEN
  path = "".join((API, "/".join([str(arg) for arg in args]), "?", urllib.urlencode(kwargs)))
  page = urllib2.build_opener().open(path)
  return json.loads(page.read())['result']


def average(reviews, attr):
  average = 0.0
  if reviews:
    for review in reviews:
      try:
        average += review[attr]
      except:
        pass
    return round(average / len(reviews), 2)
  else:
    return -1.0


def recent(reviews, attr):
  #since review can be empty dicts, we check to make sure we get something we can actually use
  while reviews:
    review = reviews.pop()
    if review:
      try:
        return round(review[attr], 2)
      except:
        return -1.0

class Review(dict):
  def __init__(self, raw_review):
    self.raw = raw_review
    super(Review, self).__init__([(attr, float(score)) for attr, score in raw_review['ratings'].items()])



class Instructor(object):
  def __init__(self, raw_instructor):
    self.name = raw_instructor['name']
    self.id = raw_instructor['id']

  @property
  def reviews(self):
    return [Review(raw_review) for raw_review in pcr('instructor', self.id, 'reviews')['values']]
  
  @property
  def sections(self):
    sections =[Section(raw_section) for raw_section in pcr('instructor', self.id, 'sections')['values']]
    sections.sort(key=lambda section: section.semester)
    return sections

  @property
  def coursehistories(self):
    return [section.course.coursehistory for section in self.sections]

  @property
  def most_recent(self):
    return self.sections[-1]
  
  def recent(self, attr):
    return recent(self.reviews, attr)


class Section(object):
  def __init__(self, raw_section):
    self.raw = raw_section
    self.id = raw_section['id']
    self.sectionnum = raw_section['sectionnum']
    self.semester = raw_section['course']['semester']

  @property
  def instructors(self):
    return [Instructor(raw_instructor) for raw_instructor in self.raw['instructors']]

  @property
  def reviews(self):
    return [Review(raw_review) for raw_review in pcr(*(self.raw['path'].split('/') + ['reviews']))['values']]

  @property
  def course(self):
    return Course(pcr('course', self.raw['course']['id']))


class Course(object):
  def __init__(self, raw_course):
    self.raw = raw_course
    self.semester = raw_course['semester']
    self.id = raw_course['id']
    self.aliases = [" ".join(alias.split('-')) for alias in raw_course['aliases']]
    self.description = raw_course['description']
  
  @property
  def name(self):
    return self.aliases[-1]

  @property
  def coursehistory(self):
    return CourseHistory(pcr(*self.raw['history']['path'].split('/')))

  @property
  def instructors(self):
    return set([instructor for section in self.sections for instructor in section.instructors])

  @property
  def sections(self):
    return set([Section(section) for section in pcr('course', self.id, 'sections')['values']
        if all([time['type'] == 'LEC' for time in section['meetingtimes']])])

  def __eq__(self, other):
    return self.id == other.id


class CourseHistory(object):
  def __init__(self, raw_coursehistory):
    self.raw = raw_coursehistory
    self.name = raw_coursehistory['name']

  @property
  def courses(self):
    return [Course(pcr('course', raw_course['id'])) for raw_course in self.raw['courses']]

  @property
  def subtitle(self):
    return self.courses[-1].aliases[0]

  @property
  def sections(self):
    return [section for instructor in self.instructors for section in instructor.sections]

  @property
  def most_recent(self):
    return self.courses[-1]

  @property
  def description(self):
    return self.most_recent.description

  @property
  def number(self):
    return self.most_recent.aliases[0]

  def __eq__(self, other):
    return self.name == other.name

  def recent(self, attr):
    return average([review for section in self.most_recent.sections for review in section.reviews], attr)
    
  @property
  def instructors(self):
    #so hacky
    unique = set()
    instructors = [instructor for course in self.courses for instructor in course.instructors]
    while instructors:
      instructor = instructors.pop()
      if instructor:
        unique.add(instructor)
        for o, other in enumerate(instructors):
          if other and instructor.id == other.id:
            instructors[o] = 0
    return unique
