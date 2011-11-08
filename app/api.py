import urllib
import urllib2
import json

from ..sandbox_config import API, TOKEN
from memoize import memoize


@memoize
def pcr(*args, **kwargs):
  kwargs["token"] = TOKEN
  path = "".join((API, "/".join([str(arg) for arg in args]), "?", urllib.urlencode(kwargs)))
  page = urllib2.build_opener().open(path)
  return json.loads(page.read())['result']


