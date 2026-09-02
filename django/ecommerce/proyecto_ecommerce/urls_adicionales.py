"""
Configuración de URLs adicionales del sitio.

Este archivo contiene las URL adicionales que no pertenecen a ninguna app específica.
Se debe agregar en config/urls.py con include().
"""

# En config/urls.py, agregar esto:
#
# from django.urls import path, include
# from . import views
#
# urlpatterns = [
#     # URLs principales del sitio
#     path('', views.inicio, name='inicio'),
#     path('acerca-de/', views.acerca_de, name='acerca_de'),
#     path('contacto/', views.contacto, name='contacto'),
#     path('terminos-servicio/', views.terminos_servicio, name='terminos'),
#     path('politica-privacidad/', views.politica_privacidad, name='privacidad'),
#
#     # URLs de aplicaciones
#     path('productos/', include('apps.productos.urls')),
#     path('usuarios/', include('apps.usuarios.urls')),
#     path('carrito/', include('apps.carrito.urls')),
#     path('pedidos/', include('apps.pedidos.urls')),
# ]
