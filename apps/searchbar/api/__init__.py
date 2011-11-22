import functools
import urllib
import urllib2
import json

from pcrsite.sandbox_config import DOMAIN, TOKEN
from dataflow import dataflow
from memoize import memoize

#dataflow makes the function return a dummy object and starts a thread for the request
#if the dummy object is asked for data, the thread blocks

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
