import logging
import os

import django

# Base paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

# Database
# Note: DATABASE_USER and DATABASE_PASSWORD are defined in the staging and
# production settings.py files. For local use, either define them in
# local_settings.py or ignore to use your local user.

DATABASES = {
    'default': {
        'NAME': 'videotext',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        'HOST': 'localhost'
    }
}

# DATABASE_ENGINE = 'postgresql_psycopg2'
# DATABASE_HOST = 'localhost'
# DATABASE_PORT = '5432'
# DATABASE_NAME = 'videotext'

# Local time
TIME_ZONE = 'America/New_York'

# Local language
LANGUAGE_CODE = 'en-us'

# Site framework
SITE_ID = 1

# Internationalization
USE_I18N = False

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')
STATIC_ROOT = os.path.join(SITE_ROOT, 'assets/static')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = 'http://media.reporterslab.org/tvn/site_media/'
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
#ADMIN_MEDIA_PREFIX = '/media/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '[[ YOUR SECRET KEY ]]'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'videotext.configs.common.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'taggit',
    'taggit_autosuggest',
    'django.contrib.sitemaps',
    'south',
    'tastypie',
    'uploadify_s3',
    'videotext.apps.core',
)

# Predefined domain
MY_SITE_DOMAIN = 'localhost:8000'

# Email
# run "python -m smtpd -n -c DebuggingServer localhost:1025" to see outgoing
# messages dumped to the terminal
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'do.not.reply@reporterslab.org'

# Caching
CACHE_MIDDLEWARE_KEY_PREFIX='videotext'
CACHE_MIDDLEWARE_SECONDS=0 # 90 minutes
CACHE_BACKEND="dummy:///"

#Grappelli
GRAPPELLI_ADMIN_TITLE = "TV"

# Django Storages
from S3 import CallingFormat
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = '[[ YOUR ACCESS KEY ID ]]'
AWS_SECRET_ACCESS_KEY = '[[ YOUR SECRET ACCESS KEY ]]'
AWS_STORAGE_BUCKET_NAME = '[[ YOUR BUCKET ]]'
AWS_STORAGE_ACL = AWS_DEFAULT_ACL = 'public-read'
AWS_DEFAULT_FORM_LIFETIME = 3600
#authorization profiles
AUTH_PROFILE_MODULE = 'videotext.apps.core.models.UserProfile'

#TastyPie
TASTYPIE_FULL_DEBUG = True


# Logging
#logging.basicConfig(
#    level=logging.DEBUG,
#)

# Allow for local (per-user) override
try:
    from local_settings import *
except ImportError:
    pass

try:
    from settings_private import * 
except ImportError:
    pass