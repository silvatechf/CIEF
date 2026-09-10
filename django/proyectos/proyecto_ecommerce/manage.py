#!/usr/bin/env python
"""
Script de gestión de Django para tareas administrativas.

Este script sirve como punto de entrada para el manejo del proyecto Django.
Permite ejecutar comandos como:
  - python manage.py runserver
  - python manage.py migrate
  - python manage.py createsuperuser
  - python manage.py makemigrations
"""

import os
import sys


def main():
    """Función principal para ejecutar comandos de Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "No se puede importar Django. ¿Está instalado y disponible en su "
            "PYTHONPATH?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
