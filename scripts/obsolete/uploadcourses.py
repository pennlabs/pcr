'''Takes a year, a semester, and registrar data scraped from download.py and updates the database appropriately.'''
#!/usr/bin/python

import re, sys, itertools, os
import datetime, time, calendar, pprint
import pickle
import MySQLdb as db

os.environ['DJANGO_SETTINGS_MODULE'] = 'api.settings'
os.environ['PYTHONPATH'] = '$(cd ..;pwd)'

sys.path.append('..')
sys.path.append("../api")

import settings, courses
from sandbox_config import *
from courses.models import *

course_histories = None
TIMETABLE = True # true if there's no rooms yet

# note: this database is only used to look up departments
conn = db.connect(db=IMPORT_DATABASE_NAME,
                  user=IMPORT_DATABASE_USER,
                  passwd=IMPORT_DATABASE_PWD)

def merge_course_histories(*chs):
  """Blindly, brutally merge all of these course histories into the first one and save"""
  correct_ch = chs[0] 
  for bad_ch in chs[1:]:
    for course in bad_ch.course_set.all():
      #can we find a similar course? if so, merge, if not, add
      #merge on 'any similar course numbers the section'?
      potential_merges = correct_ch.course_set.filter(semester=course.semester)
      section_nums = set([s.sectionnum for s in course.section_set.all()])
      merge_candidates = [m for m in potential_merges \
                            for s in m.section_set.all() \
                            if s.sectionnum in section_nums] 

      if len(merge_candidates) > 0: # found merge candidate
        merge_courses(merge_candidates[0], course) 
      else: # add this as a new valid course 
        print "adding %s to course history %s" % (course, correct_ch)
        course.history = correct_ch
        course.save()
    correct_ch.notes += "\n(Includes courses merged from %d)" % (bad_ch.id,)
  correct_ch.save()

def merge_courses(lives, dies):
  """blindly, brutally merge the two courses (c1 survives and gets c2's aliases)"""
  #move aliases, delete c2
  print "merging %s into %s" % (dies, lives)
  for alias in dies.alias_set.all():
    alias.course = lives
    alias.save()
  dies.delete()

def run_query(query_str, args=None):
  c = conn.cursor()
  c.execute(query_str, args)
  return c.fetchall()

def select(fields, table, conditions=None):
  query = "SELECT %s FROM %s" % (str.join(', ', fields), table)
  if conditions:
    query += " WHERE %s" % str.join(' AND ', conditions)
  return run_query(query)

class Importer(object):
  def timeinfo_to_times(self, starttime, endtime, meridian):
    """ Takes a start and end time, along with am/pm, returns an integer (i.e., 1200 for noon) """
        #first, split each time into list with hours as first element, minutes maybe as second

    startlist = starttime.split(':')
    endlist   = endtime.split(':')

    if meridian == 'PM':
      endlist[0] = str(int(endlist[0]) + 12)
        # if it's pm, and start time is before 8, make it a pm.. ex. 1-3PM should be 1PM-3PM
      if int(startlist[0]) <= 8:
        startlist[0] = str(int(startlist[0]) + 12)

    if len(startlist) == 1: startlist.append('00')
    if len(endlist) == 1: endlist.append('00')

    return int(''.join(startlist)), int(''.join(endlist))

  def verify_alias(self, code, crosslists, sem):
    """Check if the given alias already exists"""
    crosslists.append(code)
    for crosslist in crosslists:
      deptString, num = (part.strip() for part in crosslist.split('-'))
      try:
        dept = Department.objects.filter(code=deptString.strip())[0]
      except IndexError:
        continue
      obj = Alias.objects.filter(department=dept, 
          coursenum=num.strip(), 
          semester=Semester(YEAR, SEASON))

      if len(obj) > 0:
        return True
    return False

  def import_department(self, deptTup, season, year):
    """ Imports all the courses for a given parsed department, and saves dept info """
    global course_histories

    deptname = deptTup[0]
    courses = deptTup[1]

    if len(courses) == 0:
      return
    deptcode = courses[0]['code'].strip().split('-')[0].strip()
    sem = Semester(year, season)
    dept, _ = Department.objects.get_or_create(
        code = deptcode.strip(),
        defaults = {'name': deptname}
        )

    try:
      if not course_histories:
        course_histories = pickle.load(open("courses.p", "r"))
    except IOError:
      print "can't find courses file. " + \
        "Did you run import_from_pcr.py? that generates those"
      exit(-1)
    print "found pickle"
    for c in courses:
      self.import_course(course_histories, c, sem)

  def import_course(self, course_histories, course, sem):
    """ Imports all info for a given parsed course """
    print "llooking at %s" % (course,)

    if self.verify_alias(course['code'], course['crosslists'], sem):
      for alias in course['crosslists']:
        (deptCode, coursenum) = alias.split('-')
        courses = Alias.objects.filter(department=Department(deptCode)).filter(coursenum=coursenum).filter(semester=sem)
        if len(courses) > 0:
          new_course =  courses[0].course             
          break
    else:
      new_course = Course()

    new_course.name     = course['name']
    new_course.credits  = course['credits']
    new_course.semester = sem

    deptcode = course['code'].strip().split('-')[0].strip()
    coursecode = course['code'].strip().split('-')[1].strip()
    dept_id = select(['dept_ID'], 'coursereview_tbldepts', ["dept_code=\"" + deptcode + "\""])

    #find the relevant course history objects
    relevant_course_histories = set()
    for alias in course['crosslists']:
      (deptCode, coursenum) = alias.split('-')
      print "[%s][%s]" % (deptCode, coursenum)
      similar_aliases = Alias.objects.filter(department=Department(deptCode), coursenum=coursenum) \
        .order_by('-id') # newer first
      for similar_alias in similar_aliases:
        relevant_course_histories.add(similar_alias.course.history) 

    print "found %d relevant course histories" % (len(relevant_course_histories),)

    if len(relevant_course_histories) > 0:
      rch_list = list(relevant_course_histories)
      new_course.history = rch_list[0] 
      new_course.save()
      if len(relevant_course_histories) > 1:
        print "merging course histories! means we have bad data", rch_list
        merge_course_histories(*rch_list)
    else:
      print "Creating new history for code %s, course %s" % (course['code'], course['name'])
      new_course.history = CourseHistory.objects.create(notes = "Created from Registrar:" + str(course['code']))

    new_course.save()
    self.save_alias(course['crosslists'], new_course)
    self.save_sections(course['sections'], new_course)

  def save_alias(self, crosslists, course):
    """ This will save the alias for a given course, given a code (such as CIS-110 and the course object """
    sem = Semester(YEAR, SEASON)
    for cross in crosslists:
      if self.verify_alias(cross, [], sem):
        continue
      alias = Alias()
      alias.course = course
      deptString, num = cross.split('-')
      dept, _ = Department.objects.get_or_create(
          code = deptString.strip(),
          defaults = {'name': deptString.strip()}
          )
      alias.department = dept
      alias.coursenum  = num.strip()
      alias.semester   = sem
      alias.save()

  def save_sections(self, groups, course):
    Section.objects.filter(course=course).delete()

    for groupnum, group in enumerate(groups):
      for sectInfo in group:
        section = Section()
        section.course     = course
        section.sectionnum = sectInfo['num']
        section.group = groupnum

        section.save()
        if sectInfo['instructor']: 
          for prof in sectInfo['instructor'].split('/'):
            section.instructors.add(self.save_instructor(sectInfo['instructor']))
            section.save()

        for meeting in sectInfo['times']:
          for day in meeting[1]:
            start, end = self.timeinfo_to_times(meeting[2],
                meeting[3],
                meeting[4])

            time = MeetingTime(
                section = section,
                type = meeting[0],
                day = day,
                start = start,
                end = end,
                room = self.save_room(meeting[5] if len(meeting) > 5
                  else "TBA")
                )
            time.save()

  def save_instructor(self, name):
    """ Returns a Instructor given a name, creating if necessary """
    try:
      last, first = name.split()
    except:
      last, first = name, None
    instructor, _ = Instructor.objects.get_or_create(first_name=first, last_name=last) 
    return instructor

  def save_room(self, roomCode):
    """Return a Room given code, creating room and building if necessary"""

    # This is wrong.
    if not roomCode or roomCode == "TBA":
      roomCode = "TBA 0"

    buildCode, roomNum = roomCode.split(' ')

    building, _ = Building.objects.get_or_create(
        code = buildCode,
        defaults = {
          'name' : '',
          'latitude': 0.0,
          'longitude': 0.0
          }
        )

    room, _ = Room.objects.get_or_create(
        building = building,
        roomnum = roomNum,
        defaults = {'name': ''}
        )
    return room


class Parser(object):
  def remove_first_line(self, string):
    """ Returns everything after the first newline in a string """
    return string[string.find('\n') + 1:]

  def divide_groups(self, text):
    """ Divide text about different groups """
    return re.split('GROUP \d+ SECTIONS\n', text)

  def find_times(self, section, TIMETABLE = True):
    room = r"((?:[\w\-]+ [\w\d\-]+|TBA))"
    timeset = r"([A-Z]{3})\s+(\w+)\s+((?:[1-9]|10|11|12)(?:\:\d{2})?)-((?:[1-9]|10|11|12)(?:\:\d{2})?)(AM|PM|NOON)(?:\ +" +\
        (room if not TIMETABLE else r"") + r")?"

    time_regex = re.compile(timeset, re.M)
    return [self.parse_time(x) for x in time_regex.findall(section)]

  def parse_time(self, timeTuple, earlyInstructor=False):
    """ Converts massive tuple that find_times regexi return into something
      moderately useful. earlyInstructor is true if instructor's the
      second item in the tuple, false if 14th. """

    return timeTuple

  def find_cross_lists(self, text):
    crosslist_start = r"CROSS LISTED: "
    crosslist_end   = r"(?:SECTION MAX|MAX W/CROSS LIST)"
    restring = r"(?:(\w{2,5}\s?\s?-\d{3}).*?)+"
    regex = re.compile(restring, re.M | re.S)
    #print regex.findall(text)
    return list(set(regex.findall(text)))

  def find_sections(self, course):
    time_regex = r"^ (?:(\d{3}) (.*))"
    time_re = re.compile(time_regex, re.M)
    sections =  list(time_re.finditer(course)) # match objects for each section

    sect_combos = zip(sections, sections[1:]) # match the start of each section up with start of next

    return [course] if len(sect_combos)==0 else [course[x.start(0):y.start(0)] for x, y in sect_combos if course[x.start(0):y.start(0)].strip() != ""]

  def find_instructor(self, section):
    room = r"(?:[\w\-]+ [\w\d\-]+|TBA)"
    pattern = r" \d{3} .*?(?:AM|PM|NOON|TBA) %s (.*)" % \
      (room if TIMETABLE else "",)

    match = re.search(pattern, section)
    result =  None if match is None else match.group(1).strip()
    return result

  def find_id(self, section):
    pattern = r"^ (\d{3})"
    match = re.compile(pattern, re.M).search(section)
    return None if match is None else match.group(1).strip()

  def parse_course(self, matches):
    pass

  def parse_department(self, f, TIMETABLE=True):
    '''Parse all classes in a department.

    For example, www.upenn.edu/registrar/roster/econ.html.'''
    #record subject name to be added later
    subjname = f.readline().strip()

    # this is line one of a class
    pattern = r"^((\w{2,5}\s?\s?-\d{3})\s+(\w+.*?)\s+(?:(\d)|(\d|\d\.\d) TO (?:\d|\d\.\d)|(\d\.\d)) CU\n(.+\n)+?\s*\n)"

    regex = re.compile(pattern, re.M)
    filestr = f.read()
    matches = regex.findall(filestr)

    courses = [
        {'code'   : match[1], 
          'name'   : match[2], 
          'credits': first_true(match[3:6]),
          'groups' : self.divide_groups(self.remove_first_line(match[0])),
          'crosslists': self.find_cross_lists(self.remove_first_line(match[0])),
          'remaining' : self.remove_first_line(match[0])
          }
        for match in matches]
    return subjname, courses

  def build_courses(self, courses): 
    for course in courses:
      sect_groups  = [self.find_sections(group) for group
          in course['groups']]


      course['sections'] = [
          [
            {
              'instructor': self.find_instructor(section), 
              'times': self.find_times(section, TIMETABLE), 
              'num': self.find_id(section)
              }
            for section in group if section.strip()
            ]
          for group in sect_groups
          ]
      del course['remaining']
      del course['groups']

    return courses


def first_true(predicates):
  '''Get the first value that evaluates to True in a list.'''
  for predicate in predicates:
    if predicate:
      return predicate
  return 0

if __name__ == '__main__':
  if len(sys.argv) < 3:
    raise ValueError('Arguments should be YEAR, SEASON, FILE.')
  YEAR = sys.argv[1] #example, 2009
  SEASON = sys.argv[2] #should be either a, b, c
  print "Getting courses for %s%s" % (YEAR, SEASON)
  for file in sys.argv[3:]:
    with open(file) as f:
      p = Parser()
      subjname, parsed_courses = p.parse_department(f, TIMETABLE)

      #shouldn't be using a class like this... 
      courses = p.build_courses(parsed_courses)
      Importer().import_department((subjname, courses), SEASON, YEAR)
