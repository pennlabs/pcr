# Django settings for studyspaces project.
import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

#May override DEBUG
from sandbox_config import *

# making template path relative to allow for modular development
# thanks http://komunitasweb.com/2010/06/relative-path-for-your-django-project/
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/%s/media/' % (DISPLAY_NAME)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kwb0pv&py&-&rzw4li@+%o9e)krlmk576)u)m)m_#)@oho(d9^'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
)

ROOT_URLCONF = 'pcrsite.urls'

TEMPLATE_DIRS = (
  os.path.join(PROJECT_PATH, 'templates'),
  os.path.join(PROJECT_PATH, 'apps/pcr_detail/templates'),
  os.path.join(PROJECT_PATH, 'apps/searchbar/templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'apps.pcr_detail',
    'apps.searchbar',
    'apps.static',
)
  
if DO_STATICGENERATOR:
    MIDDLEWARE_CLASSES += ('staticgenerator.middleware.StaticGeneratorMiddleware',)
    # I think WEB_ROOT is staticgenerator-specific
    WEB_ROOT = os.path.join(PCRSITE_APP_ROOT, "staticgenerator_output/write") 
    SERVER_NAME = 'pennapps.com' # not staticgenerator-specific, but that's all that needs it
    STATIC_GENERATOR_URLS = ('.*',)
