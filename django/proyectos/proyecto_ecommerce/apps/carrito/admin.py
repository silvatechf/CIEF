"""
Configuración del admin de Django para Carrito.
"""

from django.contrib import admin
from .models import Carrito, ItemCarrito


class ItemCarritoInline(admin.TabularInline):
    """Inline para administrar items dentro del carrito."""

    model = ItemCarrito
    extra = 0
    readonly_fields = ["created_at", "updated_at"]
    fields = ["producto", "cantidad", "precio_unitario", "created_at"]


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    """Administrador personalizado para el carrito."""

    list_display = ["usuario", "cantidad_items", "total", "created_at"]
    search_fields = ["usuario__username", "usuario__email"]
    readonly_fields = ["created_at", "updated_at", "cantidad_items", "total"]
    inlines = [ItemCarritoInline]

    fieldsets = (
        ("Información", {"fields": ("usuario", "cantidad_items", "total")}),
        ("Sistema", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    """Administrador personalizado para los items del carrito."""

    list_display = ["carrito", "producto", "cantidad", "precio_unitario", "subtotal"]
    list_filter = ["created_at", "carrito__usuario"]
    search_fields = ["carrito__usuario__username", "producto__nombre"]
    readonly_fields = ["created_at", "updated_at", "subtotal"]

    fieldsets = (
        (
            "Información",
            {
                "fields": (
                    "carrito",
                    "producto",
                    "cantidad",
                    "precio_unitario",
                    "subtotal",
                )
            },
        ),
        ("Sistema", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
