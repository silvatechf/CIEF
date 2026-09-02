"""
Formularios de la aplicación de Productos.

Define los formularios para crear y editar productos.

Documentación: https://docs.djangoproject.com/es/5.0/topics/forms/
"""

from django import forms
from .models import Producto, Categoria, Imagen


class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos.

    Incluye validaciones personalizadas para el precio
    y otras características del producto.
    """

    class Meta:
        model = Producto
        fields = [
            "nombre",
            "descripcion",
            "categoria",
            "precio",
            "precio_descuento",
            "stock",
            "imagen",
            "activo",
            "destacado",
        ]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre del producto"}
            ),
            "descripcion": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Descripción detallada del producto",
                }
            ),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Precio",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "precio_descuento": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Precio con descuento (opcional)",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "stock": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Cantidad disponible",
                    "min": "0",
                }
            ),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
            "activo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "destacado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        """Validación personalizada del formulario."""
        cleaned_data = super().clean()
        precio = cleaned_data.get("precio")
        precio_descuento = cleaned_data.get("precio_descuento")

        # Validar que el precio de descuento sea menor al precio original
        if precio_descuento and precio_descuento >= precio:
            raise forms.ValidationError(
                "El precio con descuento debe ser menor al precio original."
            )

        return cleaned_data


class CategoriaForm(forms.ModelForm):
    """Formulario para crear y editar categorías."""

    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion", "imagen", "activa"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de la categoría"}
            ),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
            "activa": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ImagenForm(forms.ModelForm):
    """Formulario para agregar imágenes a la galería."""

    class Meta:
        model = Imagen
        fields = ["imagen", "orden"]
        widgets = {
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
            "orden": forms.NumberInput(attrs={"class": "form-control", "min": "0"}),
        }


class BusquedaProductoForm(forms.Form):
    """Formulario para buscar productos."""

    ORDEN_CHOICES = [
        ("-created_at", "Más recientes"),
        ("nombre", "Nombre (A-Z)"),
        ("-nombre", "Nombre (Z-A)"),
        ("precio", "Precio (menor a mayor)"),
        ("-precio", "Precio (mayor a menor)"),
    ]

    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Buscar productos..."}
        ),
    )

    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(activa=True),
        required=False,
        empty_label="Todas las categorías",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    orden = forms.ChoiceField(
        choices=ORDEN_CHOICES,
        required=False,
        initial="-created_at",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
