import os, sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
sys.path.append(PROJECT_PATH)

from sandbox_config import * 

sys.path.append(DEV_ROOT)
sys.path.append(PCRSITE_APP_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'pcrsite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
