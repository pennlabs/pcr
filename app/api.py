import urllib
import urllib2
import json

API = "http://pennapps.com/courses-ceasarb/"
TOKEN = "pennappsdemo"

def pcr(*args, **kwargs):
  kwargs["token"] = TOKEN
  path = "".join((API, "/".join([str(arg) for arg in args]), "?", urllib.urlencode(kwargs)))
  page = urllib2.build_opener().open(path)
  return json.loads(page.read())['result']
