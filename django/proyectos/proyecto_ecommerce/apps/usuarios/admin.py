"""
Configuración del admin de Django para Usuarios.

Define cómo se ven los modelos de usuarios en la interfaz de administración.
"""

from django.contrib import admin
from .models import Perfil, Direccion


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    """Administrador personalizado para el perfil de usuario."""

    list_display = ["usuario", "telefono", "ciudad", "pais", "newsletter", "created_at"]
    list_filter = ["newsletter", "created_at", "pais"]
    search_fields = ["usuario__username", "usuario__email", "telefono", "ciudad"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Información de Usuario", {"fields": ("usuario",)}),
        (
            "Información de Contacto",
            {
                "fields": (
                    "telefono",
                    "direccion",
                    "ciudad",
                    "estado",
                    "codigo_postal",
                    "pais",
                )
            },
        ),
        (
            "Perfil",
            {
                "fields": ("imagen_perfil", "bio", "newsletter"),
                "classes": ("collapse",),
            },
        ),
        (
            "Información de Sistema",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    """Administrador personalizado para las direcciones de usuario."""

    list_display = [
        "nombre",
        "usuario",
        "tipo",
        "ciudad",
        "pais",
        "predeterminada",
        "activa",
    ]
    list_filter = ["tipo", "predeterminada", "activa", "created_at", "pais"]
    search_fields = ["usuario__username", "nombre", "ciudad", "direccion"]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("Información", {"fields": ("usuario", "tipo", "nombre", "predeterminada")}),
        (
            "Dirección",
            {"fields": ("direccion", "ciudad", "estado", "codigo_postal", "pais")},
        ),
        ("Estado", {"fields": ("activa",), "classes": ("collapse",)}),
        (
            "Información de Sistema",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )
