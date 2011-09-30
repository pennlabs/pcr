
AXES = ('course', 'instructor', 'difficulty')

#Helper function to get sections table
def getSectionsTable():
  field_names = ['Semester', 'Section', 'Course', 'Instructor', 'Difficulty']
  Row = namedtuple('Row', field_names)
  row1 = Row('Fall 2010', '001', 3.0, 3.2, 2.4)
  row2 = Row('Spring 2009', '001', 3.1, 2.5, 3.2)
  return Table(field_names, [row1, row2])

COURSE = ('id', 'name')
def build_course(course):
  global COURSE
  return dict(((field, course[field]) for field in COURSE))

HISTORY = ('name',)
def build_history(history):
  global HISTORY
  return dict(((field, history[field]) for field in HISTORY))

SECTION = ('id', 'instructors',)
def build_section(section):
  global SECTION
  return dict(((field, section[field]) for field in SECTION))
