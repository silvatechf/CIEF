"""
Configuración del admin de Django para Pedidos.
"""

from django.contrib import admin
from .models import Pedido, ItemPedido, HistorialPedido, Factura


class ItemPedidoInline(admin.TabularInline):
    """Inline para administrar items dentro del pedido."""

    model = ItemPedido
    extra = 0
    readonly_fields = ["producto", "cantidad", "precio_unitario", "subtotal"]
    can_delete = False


class HistorialPedidoInline(admin.TabularInline):
    """Inline para mostrar el historial del pedido."""

    model = HistorialPedido
    extra = 0
    readonly_fields = ["estado_anterior", "estado_nuevo", "fecha"]
    can_delete = False


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """Administrador personalizado para los pedidos."""

    list_display = [
        "numero_pedido",
        "usuario",
        "estado",
        "total",
        "pagado",
        "fecha_creacion",
    ]
    list_filter = ["estado", "pagado", "fecha_creacion", "metodo_pago"]
    search_fields = ["numero_pedido", "usuario__username", "usuario__email"]
    readonly_fields = [
        "numero_pedido",
        "subtotal",
        "impuesto",
        "total",
        "fecha_creacion",
        "fecha_actualizacion",
    ]

    fieldsets = (
        (
            "Información del Pedido",
            {"fields": ("numero_pedido", "usuario", "estado", "fecha_creacion")},
        ),
        (
            "Envío",
            {"fields": ("direccion_envio", "costo_envio", "fecha_entrega_estimada")},
        ),
        ("Pago", {"fields": ("metodo_pago", "pagado", "fecha_pago")}),
        ("Totales", {"fields": ("subtotal", "impuesto", "total")}),
        ("Notas", {"fields": ("notas",), "classes": ("collapse",)}),
    )

    inlines = [ItemPedidoInline, HistorialPedidoInline]
    actions = ["marcar_como_confirmado", "marcar_como_enviado", "marcar_como_entregado"]

    def marcar_como_confirmado(self, request, queryset):
        """Acción para marcar pedidos como confirmados."""
        for pedido in queryset:
            if pedido.estado == "pendiente":
                pedido.estado = "confirmado"
                pedido.save()
                HistorialPedido.objects.create(
                    pedido=pedido,
                    estado_anterior="pendiente",
                    estado_nuevo="confirmado",
                    notas="Pedido confirmado por administrador",
                )
        self.message_user(request, "Pedidos marcados como confirmados.")

    marcar_como_confirmado.short_description = "Marcar como confirmado"

    def marcar_como_enviado(self, request, queryset):
        """Acción para marcar pedidos como enviados."""
        for pedido in queryset:
            if pedido.estado in ["confirmado", "procesando"]:
                estado_anterior = pedido.estado
                pedido.estado = "enviado"
                pedido.save()
                HistorialPedido.objects.create(
                    pedido=pedido,
                    estado_anterior=estado_anterior,
                    estado_nuevo="enviado",
                    notas="Pedido enviado",
                )
        self.message_user(request, "Pedidos marcados como enviados.")

    marcar_como_enviado.short_description = "Marcar como enviado"

    def marcar_como_entregado(self, request, queryset):
        """Acción para marcar pedidos como entregados."""
        for pedido in queryset:
            if pedido.estado == "enviado":
                pedido.estado = "entregado"
                pedido.save()
                HistorialPedido.objects.create(
                    pedido=pedido,
                    estado_anterior="enviado",
                    estado_nuevo="entregado",
                    notas="Pedido entregado",
                )
        self.message_user(request, "Pedidos marcados como entregados.")

    marcar_como_entregado.short_description = "Marcar como entregado"


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    """Administrador personalizado para los items del pedido."""

    list_display = ["pedido", "producto", "cantidad", "precio_unitario", "subtotal"]
    list_filter = ["pedido__fecha_creacion"]
    search_fields = ["pedido__numero_pedido", "producto__nombre"]
    readonly_fields = ["subtotal"]


@admin.register(HistorialPedido)
class HistorialPedidoAdmin(admin.ModelAdmin):
    """Administrador para el historial de cambios del pedido."""

    list_display = ["pedido", "estado_anterior", "estado_nuevo", "fecha"]
    list_filter = ["estado_nuevo", "fecha"]
    search_fields = ["pedido__numero_pedido"]
    readonly_fields = ["fecha"]


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    """Administrador para las facturas."""

    list_display = ["numero_factura", "pedido", "rfc", "fecha_emision"]
    list_filter = ["fecha_emision"]
    search_fields = ["numero_factura", "rfc", "pedido__numero_pedido"]
    readonly_fields = ["fecha_emision"]
