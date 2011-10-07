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


def average(items, attr):
  try:
    return sum([item[attr] for item in items]) / len(items)
  except:
    return -1.0


class Review(dict):
  def __init__(self, raw_review):
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
    return [Section(raw_section) for raw_section in pcr('instructor', self.id, 'sections')['values']]

  @property
  def coursehistories(self):
    return [section.course.coursehistory for section in self.sections]

  @property
  def most_recent(self):
    return self.sections[-1]

  def recent(self, attr):
    try:
      return self.reviews[-1][attr]
    except:
      return -1.0


  def __hash__(self):
    return hash(self.id)


class Section(object):
  def __init__(self, raw_section):
    self.raw = raw_section
    self.sectionum = raw_section['sectionnum']
    self.semester = raw_section['course']['semester']

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
    self.aliases = raw_course['aliases']

  @property
  def coursehistory(self):
    return CourseHistory(pcr(*self.raw['history']['path'].split('/')))

  @property
  def instructors(self):
    return [Instructor(instructor)
        for instructor in dict([
          (raw_instructor['id'], raw_instructor)
          for raw_section in pcr('course', self.id, "sections")['values']
          for raw_instructor in raw_section['instructors']]).values()]

  @property
  def sections(self):
    return [section for instructor in self.instructors for section in instructor.sections]


class CourseHistory(object):
  def __init__(self, raw_coursehistory):
    self.raw = raw_coursehistory
    self.name  = raw_coursehistory['name']

  @property
  def courses(self):
    return [Course(raw_course) for raw_course in self.raw['courses']]

  @property
  def subtitle(self):
    return self.courses[-1].aliases[0]

  @property
  def sections(self):
    return [section for instructor in self.instructors for section in instructor.sections]

  @property
  def most_recent(self):
    return self.courses[-1]

  def recent(self, attr):
    return average(self.most_recent, attr)
    
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
