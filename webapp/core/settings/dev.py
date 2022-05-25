import os
from .base import *

# General

SECRET_KEY = 'django-insecure-dzefd659+3zjta&&kfu#!6b41^3ek06+003nhhxqo7ef_3ibkk'

DEBUG = True

USE_TZ = False
TIME_ZONE = 'Europe/Brussels'

ALLOWED_HOSTS = ['127.0.0.1',
                'localhost',
                '10.1.12.2',
                '10.40.6.198',
                ]

INTERNAL_IPS = ['127.0.0.1', 'localhost']


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# API 42

API42_UID = os.getenv('API42_UID')
API42_SECRET = os.getenv('API42_SECRET')
API42_REDIRECT_URI = 'http://localhost:8000/authorize'
