"""
Formularios de la aplicación de Carrito.

Define los formularios para el carrito de compras.
"""

from django import forms


class AgregarAlCarritoForm(forms.Form):
    """Formulario para agregar productos al carrito."""

    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Cantidad",
                "style": "max-width: 100px;",
            }
        ),
    )
