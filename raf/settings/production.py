import os

import dj_database_url

from .base import *

# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{}'.format(
            os.path.abspath(
                os.path.join(
                    BASE_DIR, 'db.sqlite3'))),
    ),
}

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
