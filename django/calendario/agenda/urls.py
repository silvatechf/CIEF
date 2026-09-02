from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("eventos/", views.eventos, name="eventos"),
    path("eventos/nuevo/", views.evento_crear, name="evento_crear"),
    path("eventos/<int:pk>/", views.evento_detalle, name="evento_detalle"),
    path("eventos/<int:pk>/editar/", views.evento_editar, name="evento_editar"),
    path("eventos/<int:pk>/eliminar/", views.evento_eliminar, name="evento_eliminar"),
    path("eventos/<int:pk>/lembrete/", views.lembrete_evento, name="lembrete_evento"),
]
