from __future__ import division

from collections import defaultdict

from api import pcr

#TODO: Make this dynamic
CURRENT_SEMESTER = '2011C'

#we use this to provide data in the case that a course doesn't have lectures
#if a course doesn't, it will attempt to show seminar data, else lab data, else recitation data 
TYPE_RANK = ('LEC', 'SEM', 'LAB', 'REC')

class Review(object):
  def __init__(self, raw_review):
    self.raw = raw_review
    #comments really are just a block of text
    self.num_reviewers = raw_review['num_reviewers']
    self.num_students = raw_review['num_students']
    self.comments = raw_review['comments']
    for attr, score in raw_review['ratings'].items():
      setattr(self, attr, float(score))

  @property
  def instructor(self):
    return Instructor(self.raw['instructor'])

  def __repr__(self):
    return "Review(%s, %s)" % (self.raw['section']['id'], self.raw['instructor']['id'])


class Instructor(object):
  def __init__(self, raw_instructor):
    self.name = raw_instructor['name']
    self.id = raw_instructor['id']

  @property
  def last_name(self):
    return self.name.split()[-1]

  @property
  def reviews(self):
    return [Review(raw_review) for raw_review in pcr('instructor', self.id, 'reviews')['values']]
  
  @property
  def sections(self):
    raw_sections = pcr('instructor', self.id, 'sections')['values'] 
    for type_ in TYPE_RANK:
      sections = [Section(raw_section) for raw_section in raw_sections]
      if len(sections) > 0:
        break
    sections = filter(lambda section: section.semester != CURRENT_SEMESTER, sections)
    sections.sort(key=lambda section: section.semester, reverse=True)
    return sections

  @property
  def coursehistories(self):
    return [section.course.coursehistory for section in self.sections]

  @property
  def most_recent(self):
    return self.sections[-1]

  def get_sections(self, coursehistory):
    sections = filter(lambda section: section.course.coursehistory == coursehistory, self.sections)
    sections.sort(key=lambda section: section.semester, reverse=True)
    return sections

  def recent(self, attr):
    return recent(self.reviews, attr)

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
    return [Instructor(raw_instructor) for raw_instructor in self.raw['instructors']]

  @property
  def reviews(self):
    #while most sections will only have on review, it's possible that a section  has multiple
    #professors, in which case it will have multiple reviews
    return [Review(raw_review) for raw_review in pcr(*(self.raw['path'].split('/') + ['reviews']))['values']]

  @property
  def course(self):
    return Course(pcr('course', self.raw['course']['id']))

  def __repr__(self):
    return "Section(%s %s)" % (self.id, self.semester)


class Course(object):
  def __init__(self, raw_course):
    self.raw = raw_course
    self.semester = raw_course['semester']
    self.id = raw_course['id']
    self.aliases = [" ".join(alias.split('-')) for alias in raw_course['aliases']]
    self.description = raw_course['description']
  
  @property
  def name(self):
    names = set([section.name for section in self.sections])
    if len(names) == 1:
      return self.sections[-1].name
    else:
      return 'Various'

  @property
  def coursehistory(self):
    return CourseHistory(pcr(*self.raw['history']['path'].split('/')))

  @property
  def instructors(self):
    return set([instructor for section in self.sections for instructor in section.instructors])

  @property
  def sections(self):
    raw_sections = pcr('course', self.id, 'sections')['values']
    for type_ in TYPE_RANK:
      sections = [Section(raw_section) for raw_section in raw_sections]
      if len(sections) > 0:
        break
    sections = filter(lambda section: section.semester != CURRENT_SEMESTER, sections)
    sections.sort(key=lambda section: section.semester, reverse=True)
    return sections

  def __eq__(self, other):
    return self.id == other.id


class CourseHistory(object):
  def __init__(self, raw_coursehistory):
    self.raw = raw_coursehistory
    self.id = raw_coursehistory['id']
    self.name = raw_coursehistory['name']
    self.aliases = raw_coursehistory['aliases']
  
  @property
  def code(self):
    return self.aliases[0]

  @property
  def courses(self):
    return [Course(pcr('course', raw_course['id'])) for raw_course in self.raw['courses']] 

  def all_names(self):
    names = set([section.name.strip() for course in self.courses for section in course.sections])
    return names - set(['RECITATION', 'LECTURE', 'Recitation', 'Lecture']) 

  @property
  def subtitle(self):
    precondition = "" if len(self.all_names()) <= 1 else "(Most Recently) "
    return precondition + self.name 
    #heuristic clean-up: don't call it various for stupid reasons
    names = self.all_names()
    return names.pop() if len(names) == 1 else 'Various'

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
  
  def __hash__(self):
    return hash(self.id)

  def __repr__(self):
    return self.name
