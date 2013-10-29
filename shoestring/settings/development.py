from common import *

STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
	}
}

THUMBNAIL_DEBUG = True