"""
Formularios de la aplicación de Pedidos.

Define los formularios para crear y gestionar pedidos.
"""

from django import forms
from .models import Pedido


class CrearPedidoForm(forms.ModelForm):
    """Formulario para crear un nuevo pedido."""

    class Meta:
        model = Pedido
        fields = ["direccion_envio", "metodo_pago", "notas"]
        widgets = {
            "direccion_envio": forms.Select(attrs={"class": "form-control"}),
            "metodo_pago": forms.Select(attrs={"class": "form-control"}),
            "notas": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Notas especiales sobre tu pedido (opcional)",
                }
            ),
        }
