from videotext.configs.common.settings import *

# Debugging
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# Database

DATABASES = {
    'default': {
        'NAME': 'review_lab',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'PORT': '5433',
        'HOST': 'db.reporterslab.org',
        'USER': '[[ YOUR DB USER ]]',
        'PASSWORD': '[[ YOUR DB PASSWORD ]]'
    }
}




# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
# MEDIA_URL = 'http://media.reporterslab.org/videotext/'
MEDIA_URL = 'http://media.reporterslab.org/tvn/site_media/'
STATIC_URL = 'http://media.reporterslab.org/tvn/site_media/static/'

# Predefined domain
MY_SITE_DOMAIN = 'videotext.reporterslab.org'

# Email
EMAIL_HOST = 'mail.reporterslab.org'
EMAIL_PORT = 25

# Caching
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'

# S3
AWS_S3_URL = 's3://[[ your.bucket ]]/tvn/'

# logging
import logging.config
LOG_FILENAME = os.path.join(os.path.dirname(__file__), 'logging.conf')
logging.config.fileConfig(LOG_FILENAME)

