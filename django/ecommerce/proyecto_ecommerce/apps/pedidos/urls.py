"""
Configuración de URLs para la aplicación de Pedidos.
"""
from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    # Las rutas fijas deben ir antes de las rutas con variables (<str:...>)
    path("crear/", views.crear_pedido, name="crear"),
    path("", views.listar_pedidos, name="listar"),
    path("webhook/stripe/", views.stripe_webhook, name="stripe_webhook"),
    path("<str:numero_pedido>/", views.detalle_pedido, name="detalle"),
    path("<str:numero_pedido>/cancelar/", views.cancelar_pedido, name="cancelar"),
]