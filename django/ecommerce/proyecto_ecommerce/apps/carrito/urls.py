"""
Configuración de URLs para la aplicación de Carrito.

Define las rutas del carrito.
"""

from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [
    # Ver carrito
    path("", views.ver_carrito, name="ver"),
    # Agregar al carrito
    path("agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar"),
    # Actualizar carrito
    path("actualizar/", views.actualizar_carrito, name="actualizar"),
    # Eliminar del carrito
    path("eliminar/<int:item_id>/", views.eliminar_del_carrito, name="eliminar"),
    # Limpiar carrito
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
    # AJAX - Contador
    path("contador/", views.contador_carrito, name="contador"),
]
