# Django settings for PCR
import os
import raven

# For hitting the API
DOMAIN = os.getenv("DOMAIN", "http://api.penncoursereview.com/v1/")
# Otherwise, weird bugs occur wherever DOMAIN is used.
assert DOMAIN.endswith("/")

DEBUG = os.getenv("DEBUG", 'True') == 'True'
# Do static caching (true only in production)
DO_STATICGENERATOR = not DEBUG

# Personal access token for the PCR API
PCR_API_TOKEN = os.getenv("PCR_API_TOKEN")
assert PCR_API_TOKEN, "No token provided"

# Used for the /chrome/api proxy endpoint
PROXY_TOKEN = "D6cPWQc5czjT4v2Vp_h8PjFLs1OkKQ"

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "[::1]",
                 "penncoursereview.com", "www.penncoursereview.com"]

# making template path relative to allow for modular development
# thanks http://komunitasweb.com/2010/06/relative-path-for-your-django-project/
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_ENGINE = ''
# Or path to database file if using sqlite3.
DATABASE_NAME = ''
# Not used with sqlite3.
DATABASE_USER = ''
# Not used with sqlite3.
DATABASE_PASSWORD = ''
# Set to empty string for localhost. Not used with sqlite3.
DATABASE_HOST = ''
# Set to empty string for default. Not used with sqlite3.
DATABASE_PORT = ''

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
MEDIA_URL = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Path to local staticfiles
STATIC_DOC_ROOT = os.path.join(os.getcwd(), "static")

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kwb0pv&py&-&rzw4li@+%o9e)krlmk576)u)m)m_#)@oho(d9^'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        }
    }
]

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'apps.pcr_detail',
    'apps.searchbar',
    'apps.static',
    'raven.contrib.django.raven_compat'
)

if DO_STATICGENERATOR:
    MIDDLEWARE_CLASSES += \
        ('staticgenerator.middleware.StaticGeneratorMiddleware',)
    # I think WEB_ROOT is staticgenerator-specific
    WEB_ROOT = os.path.join(PROJECT_PATH, "staticgenerator_output/write")
    # not staticgenerator-specific, but that's all that needs it
    SERVER_NAME = 'pennapps.com'
    STATIC_GENERATOR_URLS = ('.*',)


# Sentry error reporting
if 'SENTRY_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.getenv('SENTRY_DSN'),
        'release': raven.fetch_git_sha(os.path.abspath(os.curdir))
    }
