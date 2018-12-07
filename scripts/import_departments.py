from collections import namedtuple
import string

#TODO: Figure out a better way to do this
#hack to get scripts to run with django
import os
import sys
sys.path.append("..")
sys.path.append("../api")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from courses.models import Department
from sandbox_config import IMPORT_DATABASE_NAME, IMPORT_DATABASE_USER, \
    IMPORT_DATABASE_PWD
from extractor import Extractor


def extract(extractor):
  fields = ('subject_code', 'subject_area_desc')
  tables = ('TEST_PCR_SUMMARY_V',)
  for code, title in extractor.select(fields, tables):
    yield code, title


def transform(row):
  return row


def load(row):
  code, title = row
  name = string.capwords(title)
  dept, _ = Department.objects.get_or_create(code=code)
  dept.name = name
  dept.save()


if __name__ == "__main__":
  extractor = Extractor(IMPORT_DATABASE_NAME, 
      IMPORT_DATABASE_USER, IMPORT_DATABASE_PWD)
  for val in extract(extractor):
    load(transform(val))
