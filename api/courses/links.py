"""Tokens for paths and dispatcher

List of keywords for each of the API end points. the API.
That is, if a user wants to get a list of Departments,
they should go to "/depts"
Our convention is to use plural names for everything.
"""

DEPARTMENT_TOKEN = 'depts'
INSTRUCTOR_TOKEN = 'instructors'
COURSEHISTORY_TOKEN = 'coursehistories'
COURSE_TOKEN = 'courses'
SECTION_TOKEN = 'sections'
REVIEW_TOKEN = 'reviews'
# TODO: This breaks convention??
BUILDING_TOKEN = 'building'
SEMESTER_TOKEN = 'semesters'

# TODO: do we want JSON keys to be here or elsewhere?
# This is the wrapper keyword for whatever is returned from the API.
# That is, if one accesses "/depts", one should get:
#   {
#       'values': [Dept1, Dept2, ...]
#   }
RSRCS = 'values'
