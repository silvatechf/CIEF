"""
Configuración de la aplicación de Pedidos.

Gestiona los pedidos de los usuarios.
"""

from django.apps import AppConfig


class PedidosConfig(AppConfig):
    """Configuración de la aplicación Pedidos."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pedidos"
    verbose_name = "Gestión de Pedidos"
