# Django settings for PCR
import os

import dj_database_url
import raven


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# For hitting the API
DOMAIN = os.getenv('DOMAIN', 'http://localhost:8000/api/')
# Otherwise, weird bugs occur wherever DOMAIN is used.
assert DOMAIN.endswith('/')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Used for the /chrome/api proxy endpoint
PROXY_TOKEN = os.getenv('PROXY_TOKEN', None)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '[::1]',
                 'penncoursereview.com', 'www.penncoursereview.com',
                 'api.penncoursereview.com']

API_HOST = 'api.penncoursereview.com'

DISPLAY_NAME = os.getenv('API_DISPLAY_NAME', '/')

# Ensure DISPLAY_NAME is never used relatively by beginning with forward slash
assert DISPLAY_NAME.startswith('/')

# making template path relative to allow for modular development
# thanks http://komunitasweb.com/2010/06/relative-path-for-your-django-project/
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))


# Necessary for `courses/management/commands/importfromisc.py` and
#               `courses/management/commands/mergeprofs.py`
IMPORT_DATABASE_NAME = os.getenv('API_IMPORT_DATABASE_NAME', 'old_pcr_2011b')
IMPORT_DATABASE_USER = os.getenv('API_IMPORT_DATABASE_USER', 'pcr-daemon')
IMPORT_DATABASE_PWD = os.getenv('API_IMPORT_DATABASE_PWD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES['default'].update(dj_database_url.config(conn_max_age=600))

if DATABASES['default']['ENGINE'].endswith('mysql'):
    DATABASES['default']['OPTIONS'] = {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Authentication Backends

AUTHENTICATION_BACKENDS = (
    'accounts.backends.LabsUserBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

USE_TZ = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
MEDIA_URL = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

# Path to local staticfiles
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.getenv('SECRET_KEY', 'kwb0pv&py&-&rzw4li@+%o9e)krlmk576)u)m)m_#)@oho(d9^')
assert SECRET_KEY, 'No secret key provided!'

MIDDLEWARE = (
    'api.middleware.ApiHostMiddleware',
    'accounts.middleware.OAuth2TokenMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'api.apiconsumer.authenticate.Authenticate',
)

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(PROJECT_PATH, 'templates'),
        ],
        'APP_DIRS': True,
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
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    'apps.pcr_detail',
    'apps.searchbar',
    'apps.static',
    'raven.contrib.django.raven_compat',

    'api.courses',
    'api.apiconsumer',
    'django_extensions',
    'accounts.apps.AccountsConfig',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

CORS_URLS_REGEX = r'^/api/.*$'


# Used for Django debug toolbar (or use debugsqlshell)
try:
    import debug_toolbar  # noqa
except ImportError:
    pass
else:
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = ('158.130.103.7', '127.0.0.1')


# Sentry error reporting
if 'SENTRY_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.getenv('SENTRY_DSN'),
        'release': raven.fetch_git_sha(os.path.abspath(os.curdir))
    }


# Disable cache in development
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


# Labs Accounts Settings
PLATFORM_ACCOUNTS = {
    'REDIRECT_URI': os.environ.get('LABS_REDIRECT_URI'),
    'ADMIN_PERMISSION': 'pcr_admin'
}

if DEBUG:
    PLATFORM_ACCOUNTS.update({
        'REDIRECT_URI': os.environ.get('LABS_REDIRECT_URI', 'http://localhost:8000/accounts/callback/'),
        'CLIENT_ID': 'clientid',
        'CLIENT_SECRET': 'supersecretclientsecret',
        'PLATFORM_URL': 'https://platform-dev.pennlabs.org',
        'CUSTOM_ADMIN': False,
    })

    # Disable https requirement for oauth in development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
else:
    PLATFORM_ACCOUNTS.update({
        'REDIRECT_URI': PLATFORM_ACCOUNTS['REDIRECT_URI'] or 'https://penncoursereview.com/accounts/callback/',
    })
