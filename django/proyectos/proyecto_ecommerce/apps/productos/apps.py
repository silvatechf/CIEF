"""
Configuración de la aplicación de Productos.

Esta aplicación gestiona todos los productos del ecommerce.
"""

from django.apps import AppConfig


class ProductosConfig(AppConfig):
    """Configuración de la aplicación Productos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.productos"
    verbose_name = "Gestión de Productos"
