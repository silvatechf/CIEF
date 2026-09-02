"""
Configuración WSGI para el proyecto Ecommerce.

Esta es la configuración para el servidor WSGI en producción.
Se usa con servidores como Gunicorn, uWSGI, etc.

Documentación: https://docs.djangoproject.com/es/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
