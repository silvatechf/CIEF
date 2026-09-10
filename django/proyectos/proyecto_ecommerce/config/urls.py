"""
Configuración de URLs principales del proyecto Ecommerce.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    
    # Inclusiones de apps específicas (van PRIMERO para evitar conflictos de captura)
    path("usuarios/", include("apps.usuarios.urls")),
    path("carrito/", include("apps.carrito.urls")),
    path("pedidos/", include("apps.pedidos.urls")),
    path("eventos/", include("apps.eventos.urls")),

    # App de productos al FINAL (porque maneja la raíz e identifica slugs dinámicos)
    path("", include("apps.productos.urls")), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Administración - Ecommerce"
admin.site.site_title = "Ecommerce Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"

