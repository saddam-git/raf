#from ..log_filters import ManagementFilter
from .base import *
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l)zht&^pddidsyqe$+09%se1*ba2#b_q-!j0^v$(-3c-=-vmq4'

DEBUG = True

ALLOWED_HOSTS = []



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Caches
# https://docs.djangoproject.com/en/1.8/topics/cache/#local-memory-caching


# Email
# https://docs.djangoproject.com/en/1.8/topics/email/

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'