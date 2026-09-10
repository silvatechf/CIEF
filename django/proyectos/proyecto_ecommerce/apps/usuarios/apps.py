"""
Configuración de la aplicación de Usuarios.

Gestiona la autenticación y perfiles de usuarios.
"""

from django.apps import AppConfig


class UsuariosConfig(AppConfig):
    """Configuración de la aplicación Usuarios."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usuarios"
    verbose_name = "Gestión de Usuarios"
