"""
Configuración de URLs para la aplicación de Productos.

Define las rutas de la aplicación.

Documentación: https://docs.djangoproject.com/es/5.0/topics/http/urls/
"""

from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    # Listado de productos
    path("", views.listar_productos, name="listar"),
    # Detalles de producto
    path("<slug:slug>/", views.detalle_producto, name="detalle"),
    # Categorías
    path("categorias/", views.listar_categorias, name="categorias"),
    # Productos destacados
    path("destacados/", views.productos_destacados, name="destacados"),
    # Vistas basadas en clases (alternativas)
    # path('cbv/listar/', views.ListaProductosView.as_view(), name='listar_cbv'),
    # path('cbv/<slug:slug>/', views.DetalleProductoView.as_view(), name='detalle_cbv'),
]
from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    # Listado de productos
    path("", views.listar_productos, name="listar"),
    
    # Categorías y Productos Destacados (Declarados ANTES del slug dinámico)
    path("categorias/", views.listar_categorias, name="categorias"),
    path("destacados/", views.productos_destacados, name="destacados"),
    
    # Detalles de producto (Siempre al final para evitar sobreescribir otras rutas)
    path("<slug:slug>/", views.detalle_producto, name="detalle"),
]