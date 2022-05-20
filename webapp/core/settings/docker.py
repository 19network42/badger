import os
from celery.schedules import crontab
from .base import *

# General

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['badger.s19.be']

INTERNAL_IPS = ['127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://badger.s19.be']

STATIC_ROOT = '/app/static/'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'level': 'DEBUG',
    'formatters': {
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# API intra.42.fr

API42_UID = os.getenv('API42_UID')
API42_SECRET = os.getenv('API42_SECRET')
API42_REDIRECT_URI = 'https://badger.s19.be/authorize'

# Celery

CELERY_BROKER_URL = 'redis://redis:6379/0'

CELERY_BEAT_SCHEDULE = {
    'update_users': {
        'task': 'accounts.tasks.update_users',
        'schedule': crontab(hour=1, minute=0, day_of_month='*', month_of_year='*', day_of_week='*')
    },
}
