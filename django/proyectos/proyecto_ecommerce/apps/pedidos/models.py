"""
Modelos de la aplicación de Pedidos.

Define los modelos para los pedidos y su historial.

Documentación: https://docs.djangoproject.com/es/5.0/topics/db/models/
"""

from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto
from apps.usuarios.models import Direccion
from decimal import Decimal
import uuid


class Pedido(models.Model):
    """
    Modelo que representa un pedido del cliente.

    Almacena información completa del pedido incluyendo
    dirección de envío, estado y total.

    Atributos:
        numero_pedido: Número único del pedido
        usuario: Usuario que realizó el pedido
        estado: Estado actual del pedido
        direccion_envio: Dirección de envío
        notas: Notas adicionales del cliente
        subtotal: Subtotal sin impuestos
        impuesto: Monto del impuesto
        total: Total del pedido
        pagado: Indica si el pedido fue pagado
        fecha_creacion: Fecha de creación
        fecha_actualizacion: Fecha de última actualización
    """

    ESTADO_CHOICES = [
        ("pendiente", "Pendiente de Confirmación"),
        ("confirmado", "Confirmado"),
        ("procesando", "Procesando"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
        ("retornado", "Retornado"),
    ]

    METODO_PAGO_CHOICES = [
        ("tarjeta", "Tarjeta de Crédito/Débito"),
        ("paypal", "PayPal"),
        ("transferencia", "Transferencia Bancaria"),
        ("efectivo", "Efectivo al Recibir"),
    ]

    numero_pedido = models.CharField(
        max_length=50, unique=True, verbose_name="Número de Pedido", editable=False
    )

    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="pedidos", verbose_name="Usuario"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="pendiente",
        verbose_name="Estado del Pedido",
    )

    direccion_envio = models.ForeignKey(
        Direccion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Dirección de Envío",
    )

    metodo_pago = models.CharField(
        max_length=20, choices=METODO_PAGO_CHOICES, verbose_name="Método de Pago"
    )

    notas = models.TextField(blank=True, verbose_name="Notas del Pedido")

    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal"
    )

    impuesto = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Impuesto (IVA)"
    )

    costo_envio = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Costo de Envío"
    )

    total = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Total"
    )

    pagado = models.BooleanField(default=False, verbose_name="¿Pagado?")

    fecha_pago = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de Pago"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Creación"
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de Actualización"
    )

    fecha_entrega_estimada = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Entrega Estimada"
    )

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["numero_pedido"]),
            models.Index(fields=["usuario", "estado"]),
            models.Index(fields=["estado", "fecha_creacion"]),
        ]

    def __str__(self):
        return f"Pedido {self.numero_pedido}"

    def save(self, *args, **kwargs):
        """Genera el número de pedido si no existe."""
        if not self.numero_pedido:
            self.numero_pedido = f"PED-{uuid.uuid4().hex[:8].upper()}"

        # Calcular totales
        items = self.items.all()
        self.subtotal = sum(item.subtotal for item in items)
        self.impuesto = self.subtotal * Decimal("0.16")  # IVA 16%
        self.total = self.subtotal + self.impuesto + self.costo_envio

        super().save(*args, **kwargs)

    def puede_cancelarse(self):
        """Retorna True si el pedido puede ser cancelado."""
        return self.estado in ["pendiente", "confirmado"]

    def puede_retornarse(self):
        """Retorna True si el pedido puede ser retornado."""
        return self.estado == "entregado"

    def marcar_como_pagado(self):
        """Marca el pedido como pagado."""
        from django.utils import timezone

        self.pagado = True
        self.fecha_pago = timezone.now()
        self.save()


class ItemPedido(models.Model):
    """
    Modelo que representa un item en el pedido.

    Guarda información del producto en el momento del pedido.

    Atributos:
        pedido: Relación con el pedido
        producto: Referencia al producto
        cantidad: Cantidad de productos
        precio_unitario: Precio del producto al momento del pedido
        subtotal: Subtotal del item
    """

    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="items", verbose_name="Pedido"
    )

    producto = models.ForeignKey(
        Producto, on_delete=models.SET_NULL, null=True, verbose_name="Producto"
    )

    cantidad = models.PositiveIntegerField(verbose_name="Cantidad")

    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio Unitario"
    )

    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Subtotal"
    )

    class Meta:
        verbose_name = "Item del Pedido"
        verbose_name_plural = "Items del Pedido"
        ordering = ["-pedido__fecha_creacion"]

    def __str__(self):
        producto_nombre = (
            self.producto.nombre if self.producto else "Producto no disponible"
        )
        return f"{self.cantidad}x {producto_nombre}"

    def save(self, *args, **kwargs):
        """Calcula el subtotal automáticamente."""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)


class HistorialPedido(models.Model):
    """
    Modelo para registrar los cambios de estado del pedido.

    Permite tracking completo del pedido a través de todos sus estados.

    Atributos:
        pedido: Relación con el pedido
        estado_anterior: Estado anterior
        estado_nuevo: Estado nuevo
        notas: Notas sobre el cambio
        fecha: Fecha del cambio
    """

    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="historial",
        verbose_name="Pedido",
    )

    estado_anterior = models.CharField(
        max_length=20, verbose_name="Estado Anterior", blank=True
    )

    estado_nuevo = models.CharField(max_length=20, verbose_name="Estado Nuevo")

    notas = models.TextField(blank=True, verbose_name="Notas")

    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")

    class Meta:
        verbose_name = "Historial del Pedido"
        verbose_name_plural = "Historiales de Pedidos"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.pedido.numero_pedido} - {self.estado_nuevo}"


class Factura(models.Model):
    """
    Modelo para guardar datos de facturación.

    Guarda información fiscal del pedido.

    Atributos:
        pedido: Relación con el pedido
        numero_factura: Número único de factura
        rfc: RFC del cliente (México)
        razon_social: Razón social del cliente
        datos_facturacion: JSON con datos adicionales de facturación
        fecha_emision: Fecha de emisión de la factura
    """

    pedido = models.OneToOneField(
        Pedido, on_delete=models.CASCADE, related_name="factura", verbose_name="Pedido"
    )

    numero_factura = models.CharField(
        max_length=50, unique=True, verbose_name="Número de Factura"
    )

    rfc = models.CharField(max_length=13, blank=True, verbose_name="RFC")

    razon_social = models.CharField(
        max_length=255, blank=True, verbose_name="Razón Social"
    )

    fecha_emision = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de Emisión"
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return f"Factura {self.numero_factura}"
