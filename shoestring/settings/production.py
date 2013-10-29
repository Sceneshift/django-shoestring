from common import *
from memcacheify import memcacheify
import os

DEBUG = False

CACHES = memcacheify()

STATIC_URL = "" #@NOTE: This should be the CDN URL, i.e. http//cdn.mydomain.com/project
STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

COMPRESS_URL = STATIC_URL
COMPRESS_ROOT = os.path.normpath(os.path.join(PROJECT_DIR, 'static'))
COMPRESS_OFFLINE = True
COMPRESS_STORAGE = STATICFILES_STORAGE