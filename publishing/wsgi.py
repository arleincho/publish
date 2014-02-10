"""
WSGI config for publishing project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os

import os
import sys
from os.path import abspath, dirname, join

ROOT_PATH = abspath(dirname(__file__))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "publishing.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = ROOT_PATH + "publishing.settings"

if ROOT_PATH not in sys.path:
    sys.path.append(ROOT_PATH)

import djcelery
djcelery.setup_loader()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
