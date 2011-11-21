import functools
import urllib
import urllib2
import json

try:
  from pcrsite.sandbox_config import DOMAIN, TOKEN
except ImportError:
  DOMAIN, TOKEN = "http://pennapps.com/courses-ceasarb/", "pcr_e4a04ecd6aaadc2fe927e00205d9b039"
from dataflow import dataflow
from memoize import memoize


@memoize
@dataflow
def api(domain, *args, **kwargs):
  path = "".join((domain, "/".join([str(arg) for arg in args]), "?", urllib.urlencode(kwargs)))
  try:
    response = urllib2.build_opener().open(path)
  except urllib2.HTTPError as e:
    raise ValueError("invalid path: %s", path)
  return json.loads(response.read())['result']
api = functools.partial(api, DOMAIN, token=TOKEN)
