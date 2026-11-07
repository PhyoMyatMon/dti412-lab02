"""ASGI config for CoursePortal."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "courseportal.settings")

application = get_asgi_application()
