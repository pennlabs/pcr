from collections import defaultdict, namedtuple
from itertools import izip, groupby, product
import re
import string
import time

import MySQLdb as db
from django.core.exceptions import ObjectDoesNotExist

#TODO: Figure out a better way to do this
#hack to get scripts to run with django
import os
import sys
sys.path.append("..")
sys.path.append("../api")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from sandbox_config import IMPORT_DATABASE_NAME, IMPORT_DATABASE_USER, \
    IMPORT_DATABASE_PWD
from courses.models import Department, Instructor, Course, Section, Review, \
    ReviewBit, Semester, CourseHistory


class Importer(object):
  def __init__(self, db):
    self.db = db
    self._depts = {}

  def _run_query(self, query_str, args=None):
    start = time.time()
    cursor = self.db.cursor()
    cursor.execute(query_str, args)
    results = cursor.fetchall()
    print query_str
    print "Took: %s" % (time.time() - start)
    print "Founds %s results.\n" % len(results)
    return results

  def _select(self, fields, tables, conditions=None,
      group_by=None, order_by=None):
    query = ["SELECT", ", ".join(fields), "FROM", ", ".join(tables)]
    if conditions:
      items = ['%s="%s"'% (k, v) for k, v in conditions.items()]
      query.extend(["WHERE", " AND ".join(items)])
          
    if group_by:
      query.extend(["GROUP BY", ", ".join(group_by)])
    if order_by:
      query.extend(["ORDER BY", ", ".join(order_by)])
    return self._run_query(" ".join(query))

  Department = namedtuple('Department', 'id code title')

  @property
  def departments(self):
    """Set of department rows.
    id - unique identifier
    code - ie, ACCT, ECON, CIS
    title - ACCOUNTING, ECONOMICS, COMPUTER & INFORMATION SCIENCE
    """
    fields = ('subject_code', 'subject_area_desc')
    tables = ('TEST_PCR_SUMMARY_V',)
    for code, title in self._select(fields, tables):
      yield self.Department(code, code, title)

  Instructor = namedtuple('Instructor', 'id first_name last_name')

  @property
  def instructors(self):
    """Set of instructor rows."""
    fields = ('instructor_penn_id', 'instructor_fname', 'instructor_lname')
    tables = ('TEST_PCR_SUMMARY_V',)
    instructors = self._select(fields, tables)
    for id, first_name, last_name in instructors:
      yield self.Instructor(id, first_name, last_name)

  Course = namedtuple('Course', 'id dept code description crosslist_ID')

  @property
  def courses(self):
    """Set of course rows."""
    fields = ('course_id', 'paragraph_number', 'course_description')
    # course_id is of form CIS110
    # course_description is split into paragraphs each with a number
    tables = ('TEST_PCR_COURSE_DESC_V',)
    order_by = ('course_id ASC', 'paragraph_number ASC')
    courses = self._select(fields, tables, order_by=order_by)

    def keyfunc(course):
      return course[0]  # id

    for id, paragraphs in groupby(courses, key=keyfunc):
      dept = re.search("[A-Z]*", id).group(0)
      code = re.search("\d+", id).group(0)
      description = "\n".join(paragraph for _, _, paragraph in paragraphs)
      # TODO: Crosslist ID
      crosslist_id = None
      yield self.Course(id, dept, code, description, crosslist_id)

  CourseHistory = namedtuple('CourseHistory', 'course_id, year, semester, section_title')

  @property
  def course_histories(self):
    fields = ('subject_code', 'course_code', 'term', 'title')
    tables = ('TEST_PCR_SUMMARY_V',)
    histories = self._select(fields, tables)
    for subject_code, course_code, term, title in histories:
      course_id = subject_code + course_code
      year = re.search("\d+", term).group(0)
      semester = re.search("[A-Z]*", term).group(0)
      yield self.CourseHistory(course_id, year, semester, title)

  Section = namedtuple("Section", \
    "year semester course_id section_code lecturer_id section_id section_title")

  def sections(self, year, semester):
    fields = ('term', 'subject_code', 'course_code', 'section_code', 'instructor_penn_id', 'section_id', 'title')
    tables = ('TEST_PCR_SUMMARY_V',)
    term = str(year) + str(semester).upper()
    conditions = {'term': term}
    sections = self._select(fields, tables, conditions)
    for term, subject_code, course_code, section_code, lecturer_id, section_id, title in sections:
      year = re.search("\d+", term).group(0)
      semester = re.search("[A-Z]*", term).group(0)
      course_id = subject_code + course_code
      yield self.Section(year, semester, course_id, section_code, lecturer_id, section_id, title)

  Review = namedtuple('Review', \
      'responses enrollment form_type course_id year semester section_code section_id lecturer_id')

  def reviews(self, year, semester):
    fields = ('responses', 'enrollment', 'form_type', 'subject_code', \
        'course_code', 'term', 'section_code', 'section_id', 'instructor_penn_id')
    tables = ('TEST_PCR_SUMMARY_V',)
    term = str(year) + str(semester).upper()
    conditions = {'term': term}
    reviews = self._select(fields, tables, conditions)
    for responses, enrollment, form_type, subject_code, course_code, term, section_code, section_id, lecturer_id in reviews:
      course_id = subject_code + course_code
      year = re.search("\d+", term).group(0)
      semester = re.search("[A-Z]*", term).group(0)
      yield self.Review(responses, enrollment, form_type, course_id, year, semester, section_code, section_id, lecturer_id)

  @property
  def _review_bit_fields(self):
    return ('rInstructorQuality', 'rCourseQuality', 'rDifficulty',
        'rCommAbility', 'rInstructorAccess', 'rReadingsValue',
        'rAmountLearned', 'rWorkRequired', 'rRecommendMajor',
        'rRecommendNonMajor', 'rArticulateGoals', 'rSkillEmphasis',
        'rHomeworkValuable', 'rExamsConsistent', 'rAbilitiesChallenged',
        'rClassPace', 'rStimulateInterest', 'rOralSkills',
        'rInstructorConcern', 'rInstructorRapport', 'rInstructorAttitude',
        'rInstructorEffective', 'rGradeFairness', 'rNativeAbility',
        'rTAQuality', 'section_ID')

  def review_bits(self, year, semester):
    fields = self._review_bit_fields
    tables = ('TEST_PCR_SUMMARY_V',)
    term = str(year) + str(semester).upper()
    conditions = {'term': term}
    return self._select(fields, tables, conditions)

  def import_departments(self):
    for dept_id, code, title in self.departments:
      dept, _ = Department.objects.get_or_create(code=code.strip())
      dept.name = string.capwords(title)
      dept.save()
      # a bit of a hack-- We can't later uniquely identify departments by
      # their old ids in future references, so we need to store their ids
      # it's possible there exists a more efficient way to store these

  def import_instructors(self):
    for oldpcr_id, first_name, last_name in self.instructors:
      Instructor.objects.get_or_create(oldpcr_id=oldpcr_id,
        first_name=first_name,
        last_name=last_name
        )

  def import_courses(self):
    # requires department was called first
    course_names = {}
    sems_taught = defaultdict(list)
    for course_id, year, semester, name in self.course_histories:
      course_names[course_id] = name
      sems_taught[course_id].append(Semester(year, semester))

    for course_id, dept_id, course_num, description, crosslist_id \
        in self.courses:
      try:
        name = course_names[course_id]
      except:
        name = course_id
      oldpcr_id = crosslist_id or course_id
      dept = Department.objects.get_or_create(code=dept_id)

      courses = set()
      for semester in sems_taught[course_id]:
        print semester, name, description
        course, _ = Course.objects.get_or_create(
            oldpcr_id=oldpcr_id,
            semester=semester,
            defaults={
              "name": name,
              "description": description,
              }
            )
        courses.add(course)

      histories = set(course.history for course in courses if course.history)
      if len(histories) > 1:
        raise "Course %d is already tied to multiple course_histories!" \
            % (course_id,)
      else:
        if histories:
          history = histories.pop()
          for course in courses:
            course.history = history
            course.save()
        else:
          for course in courses:
            course.history = CourseHistory.objects.create(
                notes="Created from PCR ID: %s" % course_id)
            course.save()

  def import_sections(self, year, semester):
    for _, _, course_id, sectionnum, lecturer_id, oldpcr_id, name \
        in self.sections(year, semester):
      section, _ = Section.objects.get_or_create(
          course=Course.objects.get(id=course_id),
          sectionnum=sectionnum,
          defaults={
            "oldpcr_id": oldpcr_id,
            "group": None,
            "sectiontype": None,
            "name": name or ""
            }
          )
      try:
        section.instructors.add(Instructor.objects.get(oldpcr_id=lecturer_id))
      except ObjectDoesNotExist:
        section.instructors.add(
            Instructor.objects.get_or_create(oldpcr_id=lecturer_id))
      section.save()

  def import_reviews(self, year, semester):
    for forms_returned, forms_produced, form_type, course_id, year, \
        semester, section_num, oldpcr_id, lecturer_id \
        in self.reviews(year, semester):
      try:
        instructor = Instructor.objects.get(id=lecturer_id)
        comments = None  # TODO: Integrate comments
        section = Section.objects.get(course__oldpcr_id=course_id)
        Review.objects.get_or_create(section=section,
         instructor=instructor,
         defaults={"forms_returned": forms_returned,
                     "forms_produced": forms_produced,
                     "form_type": form_type,
                     "comments": comments
                     }
         )
      except ObjectDoesNotExist:
        print "Can't find instructor ID: %d for review %s" \
            % (lecturer_id, section_num)

  def import_review_bits(self, year, semester):
    for review_bit_raw in self.review_bits(year, semester):
      # a review bit is a bunch of scores followed by the section id
      section_id = review_bit_raw[-1]
      review = Review.objects.get(section__id=section_id)
      if review:
        for field, score in izip(self._review_bit_fields[:-1], \
            review_bit_raw[:-1]):
          if score:
            ReviewBit.objects.get_or_create(
                review=review,
                field=field,
                score=score
                )
      else:
        print "Missing review for section: %d" % (section_id,)


if __name__ == "__main__":
  import sys
  args = sys.argv[1:]
  importer = Importer(db.connect(db=IMPORT_DATABASE_NAME, \
      user=IMPORT_DATABASE_USER, passwd=IMPORT_DATABASE_PWD))
  importer.import_departments()

  importer.import_instructors()

  importer.import_courses()

  # This is done to reduce memory overhead.
  years = range(2002, 2012)
  semesters = ('a', 'b', 'c')
  for year, semester in product(years, semesters):
    importer.import_sections(year, semester)
    importer.import_reviews(year, semester)
    importer.import_review_bits(year, semester)
