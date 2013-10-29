from datetime import date, timedelta
from memcacheify import memcacheify
import dj_database_url
import os
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

oneyr = date.today() + timedelta(days=365)

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(SITE_ROOT, os.pardir))
 
DEBUG = True

ADMINS = (

)

MANAGERS = ADMINS

DATABASES = {'default': dj_database_url.config(default='postgres://localhost:5432/{{project_name}}')}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

ALLOWED_HOSTS = ['*'] 

TIME_ZONE = 'Europe/London'
LANGUAGE_CODE = 'en-gb'
USE_I18N = False
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static/')
MEDIA_URL = ''
 
STATIC_ROOT = os.path.normpath(os.path.join(PROJECT_DIR, 'assets'))
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.normpath(os.path.join(PROJECT_DIR, 'static')),
)
 
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

#AWS_S3_CUSTOM_DOMAIN = 'cdn.domain.com' #@NOTE: Uncomment this if using a CDN such as CloudFront
AWS_ACCESS_KEY_ID = '' 
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = '' #@NOTE: The bucket name where all the files will be stored
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = False
AWS_PRELOAD_METADATA = True
AWS_LOCATION = '{{project_name}}' #@NOTE: Remove this if you want all files to go into the root of the bucket
AWS_HEADERS = {
    'Expires': oneyr.strftime('%a, %d %b %Y 20:00:00 GMT'),
    'Cache-Control': 'max-age=86400',
}

COMPRESS_OFFLINE = True

SECRET_KEY = '{{secret_key}}'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = '{{project_name}}.urls'

WSGI_APPLICATION = '{{project_name}}.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'south',
    'mptt',
    'easy_thumbnails',
    'compressor',
    'debug_toolbar',
    'suit',
    'django.contrib.admin'
)

INTERNAL_IPS = ('127.0.0.1',)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

SUIT_CONFIG = {
    "ADMIN_NAME": "{{project_name}} - Site Administration"
}

THUMBNAIL_ALIASES = {

}