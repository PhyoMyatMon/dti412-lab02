"""WSGI config for CoursePortal."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseportal.settings")

application = get_wsgi_application()
