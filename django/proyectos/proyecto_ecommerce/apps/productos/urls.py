"""
Configuración de URLs para la aplicación de Productos.
"""

from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    # Listado general accesible desde la raíz '/' y desde '/productos/'
    path("", views.listar_productos, name="listar"),
    path("productos/", views.listar_productos, name="listar_alias"),
    
    # Secciones estáticas (Antes del slug dinámico)
    path("categorias/", views.listar_categorias, name="categorias"),
    path("destacados/", views.productos_destacados, name="destacados"),
    
    # Detalles de producto por Slug (Al final)
    path("<slug:slug>/", views.detalle_producto, name="detalle"),
]