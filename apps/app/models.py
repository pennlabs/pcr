from __future__ import division
from collections import defaultdict

from api import api
from helper import capitalize


#TODO: Make this dynamic
CURRENT_SEMESTER = '2011C'

#we use this to provide data in the case that a course doesn't have lectures
#if a course doesn't, it will attempt to show seminar data, else lab data, else recitation data 
#TODO: use this
TYPE_RANK = ('LEC', 'SEM', 'LAB', 'REC')


class Review(object):
  def __init__(self, raw_review):
    self._raw = raw_review
    self.num_reviewers = raw_review['num_reviewers']
    self.num_students = raw_review['num_students']
    self.comments = raw_review['comments']
    for attr, score in raw_review['ratings'].items():
      setattr(self, attr, float(score))

  @property
  def instructor(self):
    return Instructor(self._raw['instructor']['id'])

  def __repr__(self):
    return "Review(%s, %s)" % (self._raw['section']['id'], self._raw['instructor']['id'])


class Instructor(object):
  def __init__(self, id):
    raw_instructor = api('instructor', id)
    self.name = raw_instructor['name']
    self.id = raw_instructor['id']

  @property
  def last_name(self):
    return self.name.split()[-1]

  @property
  def reviews(self):
    for raw_review in api('instructor', self.id, 'reviews')['values']:
      yield Review(raw_review) 
  
  @property
  def sections(self):
    return set(Section(raw_section) for raw_section
        in api('instructor', self.id, 'sections')['values']
        if raw_section['course']['semester'] != CURRENT_SEMESTER)

  @property
  def coursehistories(self):
    for section in self.sections:
      yield section.course.coursehistory

  def get_sections(self, coursehistory):
    for section in self.sections:
      if section.course.coursehistory == coursehistory:
      	yield section

  def recent(self, attr):
    return recent(self.reviews, attr)

  def __cmp__(self, other):
    return self.last_name > other.last_name

  def __hash__(self):
    return hash(self.id)

  def __eq__(self, other):
    return self.id == other.id

  def __repr__(self):
    return self.name


class Section(object):
  def __init__(self, raw_section):
    self.raw = raw_section
    self.id = raw_section['id']
    self.sectionnum = raw_section['sectionnum']
    self.semester = raw_section['course']['semester']
    self.name = raw_section['name']

  @property
  def instructors(self):
    for raw_instructor in self.raw['instructors']:
      yield Instructor(raw_instructor)

  @property
  def reviews(self):
    #while most sections will only have on review, it's possible that a section  has multiple
    #professors, in which case it will have multiple reviews
    for raw_review in api(*(self.raw['path'].split('/') + ['reviews']))['values']:
    	yield Review(raw_review)

  @property
  def course(self):
    return Course(self.raw['course']['id'])

  def __repr__(self):
    return "Section(%s %s)" % (self.id, self.semester)


class Course(object):
  def __init__(self, id):
    raw_course = api('course', id)
    self.raw = raw_course
    self.semester = raw_course['semester']
    self.id = raw_course['id']
    self.aliases = set(alias for alias in raw_course['aliases'])
    self.description = raw_course['description']
  
  @property
  def name(self):
    names = set(section.name for section in self.sections)
    if len(names) == 1:
      return names.pop()
    else:
      return 'Various'

  @property
  def coursehistory(self):
    for alias in self.aliases:
      return CourseHistory(alias)

  @property
  def instructors(self):
    return set(instructor for section in self.sections for instructor in section.instructors)

  @property
  def sections(self):
    return set(Section(raw_section) for raw_section
        in api('course', self.id, 'sections')['values']
        if raw_section['course']['semester'] != CURRENT_SEMESTER)

  def __eq__(self, other):
    return self.id == other.id

  def __repr__(self):
    return 'Course(%s)' % self.name


class CourseHistory(object):
  def __init__(self, title):
    raw_coursehistory = api('coursehistory', title)
    self.raw = raw_coursehistory
    self.id = raw_coursehistory['id']
    self.name = raw_coursehistory['name']
    self.aliases = set(raw_coursehistory['aliases'])
  
  @property
  def code(self):
    return iter(self.aliases).next()

  @property
  def courses(self):
    return set(Course(raw_course['id']) for raw_course in self.raw['courses'])

  def all_names(self):
    names = set([section.name.strip() for course in self.courses for section in course.sections])
    return names - set(['RECITATION', 'LECTURE', 'Recitation', 'Lecture']) 

  @property
  def subtitle(self):
    precondition = "" if len(self.all_names()) <= 1 else "(Recent Example) "
    return precondition + capitalize(self.name)

  @property
  def description(self):
    #step 1. find relevant course description
    #assumption: courses are sorted
    def first_that(collection, condition):
      for entry in collection:
        if condition(entry): 
          return entry
      return None
    
    course_w_description = first_that(self.courses, lambda x: x.description)
    description = course_w_description.description if course_w_description else ""
    return description

  def __eq__(self, other):
    return self.id == other.id

  @property
  def instructors(self):
    return set(instructor for course in self.courses for instructor in course.instructors)
  
  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return self.name
