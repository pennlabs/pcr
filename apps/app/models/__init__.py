from __future__ import division
import itertools

from api import api

#NOTE: I use sets rather than generators to reduce blocking calls.

#we use this to provide data in the case that a course doesn't have lectures
#if a course doesn't, it will attempt to show seminar data, else lab data, else recitation data 
#TODO: use this
TYPE_RANK = ('LEC', 'SEM', 'LAB', 'REC')


class Review(object):
  def __init__(self, section_id, instructor_id):
    course_id, section_id = section_id.split("-")
    try:
      raw_self = api('course', course_id, 'section', section_id, 'review', instructor_id)
    except ValueError as e:
      raise e
    else:
      self.comments = raw_self['comments']
      self.num_students = raw_self['num_students']
      self.num_reviewers = raw_self['num_reviewers']
      self.ratings = {}
      for attr, score in raw_self['ratings'].items():
        self.ratings[attr] = float(score)
      self.__instructor_id = raw_self['instructor']['id']
      self.__section_id = raw_self['section']['id']

  @property
  def instructor(self):
    return Instructor(self.__instructor_id)

  @property
  def section(self):
    return Section(self.__section_id)

  def __repr__(self):
    return "Review(%s, %s)" % (self.__instructor_id, self.__section_id)


class Instructor(object):
  def __init__(self, id):
    try:
      raw_self = api('instructor', id)
    except ValueError as e:
      raise e
    else:
      self.id = id
      self.name = raw_self['name']

  @property
  def last_name(self):
    return self.name.split()[-1]

  @property
  def sections(self):
    #TODO: Request change
    raw_sections = api('instructor', self.id, 'sections')
    return set(Section(raw_section['id']) for raw_section in raw_sections)

  @property
  def reviews(self):
    return set(Review(raw_review['section']['id'], self.id) for raw_review in api('instructor', self.id, 'reviews')['values'])

  @property
  def url(self):
    return 'instructor/%s' % self.id

  def __cmp__(self, other):
    return 1 if self.last_name > other.last_name else 0 if self.last_name == other.last_name else -1

  def __eq__(self, other):
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return "Instructor(%s)" % self.name


class Section(object):
  def __init__(self, sid):
    course_id, section_id = sid.split("-")
    try:
      raw_self = api('course', course_id, 'section', section_id)
    except ValueError as e:
      raise e
    else:
      self.id = raw_self['id']
      self.name = raw_self['name']
      self.sectionnum = raw_self['sectionnum']
      self.__course_id = raw_self['course']['id']
      self.__instructor_ids = [raw_instructor['id']
          for raw_instructor in raw_self['instructors']]

  @property
  def course(self):
    return Course(self.__course_id)

  @property
  def instructors(self):
    return set(Instructor(instructor_id) for instructor_id in self.__instructor_ids)

  @property
  def reviews(self):
    return set(Review(self.id, raw_review['instructor']['id'])
        for raw_review
        in api('course', self.__course_id, 'section', self.sectionnum, 'reviews')['values'])

  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return "Section(%s)" % self.id


class Course(object):
  def __init__(self, id):
    try:
      raw_self = api('course', id)
    except ValueError as e:
      raise e
    else:
      self.id = raw_self['id']
      self.aliases = set(alias for alias in raw_self['aliases'])
      self.description = raw_self['description']
      self.semester = raw_self['semester']
      self.__coursehistory_id = raw_self['history']['path'].split("/")[-1]
      self.__section_ids = [raw_section['id']
          for raw_section in raw_self['sections']['values']]

  @property
  def coursehistory(self):
    return CourseHistory(self.__coursehistory_id)

  @property
  def sections(self):
    return set(Section(section_id) for section_id in self.__section_ids)

  def __cmp__(self, other):
    return 1 if self.semester > other.semester else 0 if self.semester == other.semester else -1

  def __eq__(self, other):
    return self.id == other.id

  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return 'Course(%s)' % self.id


class CourseHistory(object):
  def __init__(self, id):
    #constructor id can either be one if its aliases, or numeric id
    try:
      raw_self = api('coursehistory', id)
    except ValueError as e:
      raise e
    else:
      self.id = raw_self['id']
      self.aliases = set(raw_self['aliases'])
      self.name = raw_self['name'] #ie PROG LANG AND TECH II
      self.__course_ids = [int(raw_course['id'])
          for raw_course in raw_self['courses']]

  @property
  def courses(self):
    return set(Course(course_id) for course_id in self.__course_ids)

  @property
  def alias(self):
    for alias in self.aliases:
      return alias

  @property
  def description(self):
    for course in sorted(self.courses, reverse=True):
      if course.description:
        return course.description
    return None
  
  @property
  def url(self):
    return "course/%s" % self.alias

  def __eq__(self, other):
    return self.id == other.id

  def __cmp__(self, other):
    return 1 if self.id > other.id else 0 if self.id == other.id else -1
  
  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return 'CourseHistory(%s)' % self.id
