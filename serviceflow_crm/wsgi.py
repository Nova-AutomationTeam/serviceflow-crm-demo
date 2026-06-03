"""WSGI config for ServiceFlow CRM."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "serviceflow_crm.settings")

application = get_wsgi_application()
