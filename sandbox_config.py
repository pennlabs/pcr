"""
NOTE: this is a development-specific file that lets us set various variables
(such as branch name, etc) so that we can share changes in the more general
django.wsgi and settings.py files without fear. This should be configured per-
sandbox. This and nothing else.
Author: AMK, Dec 27, 2010"""


import os

DISPLAY_NAME = "pcr" # i.e., pennapps.com/display_name
DEV_ROOT = "/var/www/pennapps.com/django" # root of all apps you're working on
PCRSITE_APP_ROOT = os.path.join(DEV_ROOT, "pcr")

#For hitting the API
DOMAIN = "http://pennapps.com/courses/"
assert DOMAIN.endswith("/") # Else, weird bugs occur wherever DOMAIN is used.
TOKEN = "this-is-not-a-token" # fill in
STATIC_DOC_ROOT = STATIC_DOC_ROOT = os.path.join(os.getcwd(), 'media')
# Do static caching (true only in production)
DO_STATICGENERATOR = False
