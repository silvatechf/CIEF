"""
Modelos de la aplicación de Carrito.

Define los modelos para el carrito de compras.

Documentación: https://docs.djangoproject.com/es/5.0/topics/db/models/
"""

from django.db import models
from django.contrib.auth.models import User
from apps.productos.models import Producto
from decimal import Decimal


class Carrito(models.Model):
    """
    Modelo que representa el carrito de compras de un usuario.

    Almacena los items que el usuario ha añadido al carrito.

    Atributos:
        usuario: Relación con el usuario propietario del carrito
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="carrito", verbose_name="Usuario"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Carrito"
        verbose_name_plural = "Carritos"

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def cantidad_items(self):
        """Retorna la cantidad total de items en el carrito."""
        return sum(item.cantidad for item in self.items.all())

    @property
    def total(self):
        """Calcula el total del carrito."""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_con_impuesto(self):
        """Calcula el total con impuesto (IVA 16%)."""
        impuesto = self.total * Decimal("0.16")
        return self.total + impuesto

    def limpiar(self):
        """Elimina todos los items del carrito."""
        self.items.all().delete()


class ItemCarrito(models.Model):
    """
    Modelo que representa un item en el carrito.

    Cada item es un producto con una cantidad específica.

    Atributos:
        carrito: Relación con el carrito
        producto: Relación con el producto
        cantidad: Cantidad de productos
        precio_unitario: Precio unitario al momento de añadir
        created_at: Fecha de creación
        updated_at: Fecha de actualización
    """

    carrito = models.ForeignKey(
        Carrito, on_delete=models.CASCADE, related_name="items", verbose_name="Carrito"
    )

    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, verbose_name="Producto"
    )

    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    precio_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio Unitario"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Item del Carrito"
        verbose_name_plural = "Items del Carrito"
        unique_together = ["carrito", "producto"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"

    @property
    def subtotal(self):
        """Calcula el subtotal del item."""
        return self.cantidad * self.precio_unitario

    def aumentar_cantidad(self, cantidad=1):
        """Aumenta la cantidad del item."""
        self.cantidad += cantidad
        self.save()

    def reducir_cantidad(self, cantidad=1):
        """Reduce la cantidad del item."""
        if self.cantidad > cantidad:
            self.cantidad -= cantidad
            self.save()
        else:
            self.delete()

    def save(self, *args, **kwargs):
        """Guarda el precio unitario si es la primera vez."""
        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio_final
        super().save(*args, **kwargs)
