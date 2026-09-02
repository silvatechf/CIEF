"""
Configuración del admin de Django para Productos.

Define cómo se ven los modelos en la interfaz de administración.

Documentación: https://docs.djangoproject.com/es/5.0/ref/contrib/admin/
"""

from django.contrib import admin
from .models import Categoria, Producto, Imagen


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Administrador personalizado para la categoría.
    """

    list_display = ["nombre", "activa", "cantidad_productos", "created_at"]
    list_filter = ["activa", "created_at"]
    search_fields = ["nombre", "descripcion"]
    readonly_fields = ["slug", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("nombre",)}

    def cantidad_productos(self, obj):
        """Muestra la cantidad de productos en la categoría."""
        return obj.productos.count()

    cantidad_productos.short_description = "Productos"


class ImagenInline(admin.TabularInline):
    """
    Inline para administrar imágenes dentro del producto.

    Permite agregar/editar imágenes directamente en la página
    de edición del producto.
    """

    model = Imagen
    extra = 1
    fields = ["imagen", "orden"]
    ordering = ["orden"]


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Administrador personalizado para los productos.

    Incluye configuración avanzada para gestión eficiente
    de productos.
    """

    list_display = [
        "nombre",
        "categoria",
        "precio_display",
        "stock_display",
        "activo",
        "destacado",
        "created_at",
    ]
    list_filter = [
        "activo",
        "destacado",
        "categoria",
        "created_at",
    ]
    search_fields = ["nombre", "descripcion", "slug"]
    readonly_fields = ["slug", "created_at", "updated_at"]
    prepopulated_fields = {"slug": ("nombre",)}

    fieldsets = (
        (
            "Información Básica",
            {"fields": ("nombre", "descripcion", "slug", "categoria")},
        ),
        ("Precio y Stock", {"fields": ("precio", "precio_descuento", "stock")}),
        ("Imágenes", {"fields": ("imagen",)}),
        ("Estado", {"fields": ("activo", "destacado"), "classes": ("collapse",)}),
        (
            "Información de Sistema",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    inlines = [ImagenInline]

    # Acciones personalizadas
    actions = ["marcar_como_activo", "marcar_como_inactivo", "marcar_como_destacado"]

    def precio_display(self, obj):
        """Muestra el precio del producto."""
        if obj.tiene_descuento:
            return f"{obj.precio} → {obj.precio_final}"
        return str(obj.precio)

    precio_display.short_description = "Precio"

    def stock_display(self, obj):
        """Muestra el stock con color según disponibilidad."""
        if obj.stock > 20:
            color = "green"
        elif obj.stock > 5:
            color = "orange"
        else:
            color = "red"
        return f'<span style="color: {color};"><b>{obj.stock}</b></span>'

    stock_display.short_description = "Stock"
    stock_display.allow_tags = True

    def marcar_como_activo(self, request, queryset):
        """Acción para marcar productos como activos."""
        cantidad = queryset.update(activo=True)
        self.message_user(request, f"{cantidad} producto(s) marcado(s) como activo.")

    marcar_como_activo.short_description = "Marcar como activo"

    def marcar_como_inactivo(self, request, queryset):
        """Acción para marcar productos como inactivos."""
        cantidad = queryset.update(activo=False)
        self.message_user(request, f"{cantidad} producto(s) marcado(s) como inactivo.")

    marcar_como_inactivo.short_description = "Marcar como inactivo"

    def marcar_como_destacado(self, request, queryset):
        """Acción para marcar productos como destacados."""
        cantidad = queryset.update(destacado=True)
        self.message_user(request, f"{cantidad} producto(s) marcado(s) como destacado.")

    marcar_como_destacado.short_description = "Marcar como destacado"


@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    """Administrador para las imágenes de productos."""

    list_display = ["producto", "orden", "created_at"]
    list_filter = ["created_at", "producto__categoria"]
    search_fields = ["producto__nombre"]
    ordering = ["producto", "orden"]

    fieldsets = (
        ("Información", {"fields": ("producto", "imagen", "orden")}),
        (
            "Información de Sistema",
            {"fields": ("created_at",), "classes": ("collapse",)},
        ),
    )
