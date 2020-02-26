from collections import defaultdict
from itertools import groupby
import re

#TODO: Figure out a better way to do this
#hack to get scripts to run with django
import os
import sys
sys.path.append("..")
sys.path.append("../api")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from courses.models import Course, Semester, Department, CourseHistory
from sandbox_config import IMPORT_DATABASE_NAME, IMPORT_DATABASE_USER, \
    IMPORT_DATABASE_PWD
from extractor import Extractor


def extract_courses(extractor):
    fields = ('course_id', 'paragraph_number', 'course_description')
    # course_id is of form CIS110
    # course_description is split into paragraphs each with a number
    tables = ('TEST_PCR_COURSE_DESC_V',)
    order_by = ('course_id ASC', 'paragraph_number ASC')
    courses = extractor.select(fields, tables, order_by=order_by)

    def keyfunc(course):
      return course[0]  # id

    for id, paragraphs in groupby(courses, key=keyfunc):
      dept = re.search("[A-Z]*", id).group(0)
      code = re.search("\d+", id).group(0)
      description = "\n".join(paragraph for _, _, paragraph in paragraphs)
      # TODO: Crosslist ID
      crosslist_id = None
      yield id, dept, code, description, crosslist_id


def extract_course_histories(extractor):
  fields = ('subject_code', 'course_code', 'term', 'title')
  # subject code is of form CIS
  # course code is of form 110
  # term is of form 2011A
  # title is of form INTERMEDIATE FRENCH II
  tables = ('TEST_PCR_SUMMARY_V',)
  histories = extractor.select(fields, tables)
  # course_id is given by course title and number, ie FNAR 123 VIDEO I
  for subject_code, course_code, term, title in histories:
    try:
      course_id = subject_code + course_code + title
    except TypeError:
      # title can be null
      course_id = subject_code + course_code
      print "% has no title!" % course_id
      title = course_id
    year = re.search("\d+", term).group(0)
    semester = re.search("[A-Z]*", term).group(0)
    yield course_id, year, semester, title


def load(raw_courses, raw_course_histories):
  # requires department was called first
  course_names = {}
  sems_taught = defaultdict(list)
  for course_id, year, semester, name in raw_course_histories:
    course_names[course_id] = name
    sems_taught[course_id].append(Semester(year, semester))

  for course_id, dept_id, course_num, description, crosslist_id \
      in raw_courses:
    try:
      name = course_names[course_id]
    except KeyError:
      name = course_id
    dept = Department.objects.get_or_create(code=dept_id)

    courses = set()
    for semester in sems_taught[course_id]:
      course, _ = Course.objects.get_or_create(
          name=name,
          semester=semester,
          defaults={
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
        history = histories.pop()  # select an arbritrary element
      else:
        history = CourseHistory.objects.create(
          notes="Created from PCR ID: %s" % course_id)
      for course in courses:
        course.history = history
        course.save()


if __name__ == "__main__":
  extractor = Extractor(IMPORT_DATABASE_NAME, IMPORT_DATABASE_USER, IMPORT_DATABASE_PWD)
  load(extract_courses(extractor), extract_course_histories(extractor))
