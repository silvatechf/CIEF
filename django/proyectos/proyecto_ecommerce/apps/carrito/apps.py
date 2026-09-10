"""
Configuración de la aplicación de Carrito.

Gestiona el carrito de compras de los usuarios.
"""

from django.apps import AppConfig


class CarritoConfig(AppConfig):
    """Configuración de la aplicación Carrito."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.carrito"
    verbose_name = "Gestión del Carrito"
