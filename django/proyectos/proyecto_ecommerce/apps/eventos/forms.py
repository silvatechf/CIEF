from django import forms
from .models import Evento


class FiltroEventosForm(forms.Form):
    """Formulario para filtrar eventos."""
    
    TIPO_CHOICES = [("", "Todos los tipos")] + list(Evento._meta.get_field("tipo").choices)
    
    tipo = forms.ChoiceField(
        choices=TIPO_CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    fecha_desde = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        })
    )
    
    fecha_hasta = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            "class": "form-control",
            "type": "datetime-local"
        })
    )
    
    usuario = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Buscar por usuario"
        })
    )
