import urllib
import urllib2
import json

from ...sandbox_config import API, TOKEN
from dataflow import dataflow
from memoize import memoize


@memoize
@dataflow
def api(*args, **kwargs):
  kwargs["token"] = TOKEN
  path = "".join((API, "/".join([str(arg) for arg in args]), "?", urllib.urlencode(kwargs)))
  try:
    response = urllib2.build_opener().open(path)
  except urllib2.HTTPError as e:
    raise e
  return json.loads(response.read())['result']
