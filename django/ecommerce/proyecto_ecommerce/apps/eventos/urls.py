from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("mis-eventos/", views.listar_mis_eventos, name="mis_eventos"),
    path("", views.EventoListView.as_view(), name="lista"),
]
