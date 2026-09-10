"""
Configuración de URLs para la aplicación Carrito.
"""
from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [
    path("", views.ver_carrito, name="ver"),
    path("agregar/<int:producto_id>/", views.agregar_al_carrito, name="agregar"),
    path("actualizar/", views.actualizar_carrito, name="actualizar"),
    path("eliminar/<int:item_id>/", views.eliminar_del_carrito, name="eliminar"),
    path("limpiar/", views.limpiar_carrito, name="limpiar"),
    path("contador/", views.contador_carrito, name="contador"),
]