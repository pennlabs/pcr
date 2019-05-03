from collections import namedtuple
import string

#TODO: Figure out a better way to do this
#hack to get scripts to run with django
import os
import sys
sys.path.append("..")
sys.path.append("../api")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import MySQLdb as db

from courses.models import Instructor
from sandbox_config import IMPORT_DATABASE_NAME, IMPORT_DATABASE_USER, \
    IMPORT_DATABASE_PWD
from extractor import Extractor


def extract(extractor):
  fields = ('instructor_penn_id', 'instructor_fname', 'instructor_lname')
  tables = ('TEST_PCR_SUMMARY_V',)
  instructors = extractor.select(fields, tables)
  for id, first_name, last_name in instructors:
    yield id, first_name, last_name


def load(row):
  oldpcr_id, first_name, last_name = row
  Instructor.objects.get_or_create(
    oldpcr_id=oldpcr_id,
    first_name=first_name,
    last_name=last_name
    )


if __name__ == "__main__":
  extractor = Extractor(db.connect(db=IMPORT_DATABASE_NAME, \
      user=IMPORT_DATABASE_USER, passwd=IMPORT_DATABASE_PWD))
  for val in extract(extractor):
    load(val)
