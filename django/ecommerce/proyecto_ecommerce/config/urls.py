"""
Configuración de URLs principales del proyecto Ecommerce.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.productos.views import listar_productos

urlpatterns = [
    # Ruta raíz
    path("", listar_productos, name="inicio"),
    
    # Admin
    path("admin/", admin.site.urls),
    
    # Inclusiones de apps (GARANTIR QUE NÃO HÁ LOOPS AQUI)
    path("productos/", include("apps.productos.urls")),
    path("usuarios/", include("apps.usuarios.urls")),
    path("carrito/", include("apps.carrito.urls")),
    path("pedidos/", include("apps.pedidos.urls")),
    path("eventos/", include("apps.eventos.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Administración - Ecommerce"
admin.site.site_title = "Ecommerce Admin"
admin.site.index_title = "Bienvenido al Panel de Administración"