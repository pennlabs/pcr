import os,sys

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

sys.path.append(PROJECT_PATH)

#Uncomment these two lines to use virtualenv
#activate_this = os.path.join(BASE_DIR, "ENV/bin/activate_this.py")
#execfile(activate_this, dict(__file__=activate_this))

BASE_DIR = os.path.realpath(os.path.dirname(PROJECT_PATH))

sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
