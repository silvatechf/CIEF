"""
Formularios de la aplicación de Usuarios.

Define los formularios para registro, perfil y direcciones.

Documentación: https://docs.djangoproject.com/es/5.0/topics/forms/
"""

from django import forms
from django.contrib.auth.models import User
from .models import Perfil, Direccion


class RegistroForm(forms.ModelForm):
    """Formulario para el registro de nuevos usuarios."""

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Contraseña"}
        ),
    )

    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Confirmar contraseña"}
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre de usuario"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Correo electrónico"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Apellido"}
            ),
        }

    def clean(self):
        """Validación personalizada del formulario."""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Validar que las contraseñas coincidan
        if password and password_confirm:
            if password != password_confirm:
                raise forms.ValidationError("Las contraseñas no coinciden.")

        # Validar que el usuario no existe
        username = cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya existe.")

        # Validar que el email no existe
        email = cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")

        return cleaned_data


class PerfilForm(forms.ModelForm):
    """Formulario para editar el perfil del usuario."""

    class Meta:
        model = Perfil
        fields = [
            "telefono",
            "direccion",
            "ciudad",
            "estado",
            "codigo_postal",
            "pais",
            "imagen_perfil",
            "bio",
            "newsletter",
        ]
        widgets = {
            "telefono": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Teléfono"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dirección"}
            ),
            "ciudad": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ciudad"}
            ),
            "estado": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Estado/Provincia"}
            ),
            "codigo_postal": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código Postal"}
            ),
            "pais": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "País"}
            ),
            "imagen_perfil": forms.FileInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Cuéntanos sobre ti...",
                }
            ),
            "newsletter": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class DireccionForm(forms.ModelForm):
    """Formulario para crear y editar direcciones."""

    class Meta:
        model = Direccion
        fields = [
            "tipo",
            "nombre",
            "direccion",
            "ciudad",
            "estado",
            "codigo_postal",
            "pais",
            "predeterminada",
        ]
        widgets = {
            "tipo": forms.Select(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nombre descriptivo"}
            ),
            "direccion": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Dirección completa"}
            ),
            "ciudad": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ciudad"}
            ),
            "estado": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Estado/Provincia"}
            ),
            "codigo_postal": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Código Postal"}
            ),
            "pais": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "País"}
            ),
            "predeterminada": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
