"""
Django settings for facenew project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
import sys
from os.path import abspath, dirname, join

ROOT_PATH = abspath(dirname(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b#0ijchgrq5@&t!2$h+1j=-d6#y0k2jyfog3baw+^zy5r!6_3h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '54.235.154.174',
    'colaboradores.nethub.co'
]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'fandjango',
    'facenew.tasks',
    'import_export',
    'facenew.whatsapp'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'fandjango.middleware.FacebookMiddleware'
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)

ROOT_URLCONF = 'facenew.urls'

WSGI_APPLICATION = 'facenew.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'alquiler_perfil',
        'USER': 'Dj4ngoU53rD4t4b4s3',
        'PASSWORD': 'Fvnja32QpxEZ5ppJYPmfP8umKKJGT2wH',
        'HOST': 'localhost',
        'PORT': '',                      # Set to empty string for default.
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = (
    ('es', 'Espanol'),
)
LANGUAGE_CODE = 'es'
LOCALE_PATHS = (
    ROOT_PATH + '/locale',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

APPEND_SLASH=False

STATIC_URL = '/static/'

MEDIA_ROOT = ROOT_PATH + '/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = ROOT_PATH + '/static/'

TEMPLATE_DIRS = (
    join(ROOT_PATH, 'templates'),
)

FACEBOOK_APPLICATION_ID = '578866438858254'
FACEBOOK_APPLICATION_SECRET_KEY = '47221ab99e0e4751f67f0bf8e26add68'
FACEBOOK_APPLICATION_NAMESPACE = 'donaangelarobledo'
FANDJANGO_SITE_URL = 'http://google.com'

FACEBOOK_APPLICATION_INITIAL_PERMISSIONS = ['publish_stream']

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "celery",
    "taskmeta_collection": "my_taskmeta" # Collection name to use for task output
}

CELERY_IMPORTS = ("facenew.tasks.tasks")

# The default Django db scheduler
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'