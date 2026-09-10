"""
Configuração de URLs para a aplicação de Pedidos.
"""
from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path("crear/", views.crear_pedido, name="crear"),
    path("mis-pedidos/", views.listar_pedidos, name="listar"),
    path("<str:numero_pedido>/", views.detalle_pedido, name="detalle"),
    path("<str:numero_pedido>/cancelar/", views.cancelar_pedido, name="cancelar"),
    path("webhook/stripe/", views.stripe_webhook, name="stripe_webhook"),
]