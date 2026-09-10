"""
Configuración de URLs para la aplicación de Usuarios.

Define las rutas de la aplicación de usuarios.
"""

from django.urls import path
from . import views

app_name = "usuarios"

urlpatterns = [
    # Registro y autenticación
    path("registrarse/", views.registrarse, name="registrarse"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Perfil
    path("perfil/", views.perfil, name="perfil"),
    # Direcciones
    path("direcciones/", views.listar_direcciones, name="direcciones"),
    path("direcciones/crear/", views.crear_direccion, name="crear_direccion"),
    path(
        "direcciones/<int:id>/editar/", views.editar_direccion, name="editar_direccion"
    ),
    path(
        "direcciones/<int:id>/eliminar/",
        views.eliminar_direccion,
        name="eliminar_direccion",
    ),
]
