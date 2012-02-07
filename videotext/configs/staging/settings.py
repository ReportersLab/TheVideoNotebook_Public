from videotext.configs.common.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database

DATABASES = {
    'default': {
        'NAME': 'videotext',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5432',
        'HOST': 'localhost',
        'USER': '[[ YOUR DB USER ]]',
        'PASSWORD': '[[ YOUR DB PASSWORD ]]'
    }
}



# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = 'http://media.beta.reporterslab.org/videotext/'
MEDIA_URL = 'http://media.reporterslab.org/tvn/site_media/'
STATIC_URL = 'http://media.reporterslab.org/beta/tvn/site_media/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"


# Predefined domain
MY_SITE_DOMAIN = 'vt.beta.reporterslab.org'

# Email
EMAIL_HOST = 'mail.beta.reporterslab.org'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# S3
AWS_S3_URL = 's3://[[ your.bucket ]]/beta/videotext/'


# Trib IPs for security
INTERNAL_IPS = ()

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)

