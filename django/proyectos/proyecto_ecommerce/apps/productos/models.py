"""
Modelos de la aplicación de Productos.

Define los modelos principales para productos y categorías del ecommerce.

Documentación: https://docs.djangoproject.com/es/5.0/topics/db/models/
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from decimal import Decimal


class Categoria(models.Model):
    """
    Modelo que representa una categoría de productos.

    Una categoría agrupa productos relacionados para facilitar
    la navegación en el ecommerce.

    Atributos:
        nombre: Nombre único de la categoría
        descripcion: Descripción detallada de la categoría
        imagen: Imagen representativa de la categoría
        slug: Identificador amigable para URLs
        activa: Indica si la categoría está activa
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    nombre = models.CharField(
        max_length=100, unique=True, verbose_name="Nombre de la categoría"
    )
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    imagen = models.ImageField(
        upload_to="categorias/",
        blank=True,
        null=True,
        verbose_name="Imagen de la categoría",
    )
    slug = models.SlugField(unique=True, verbose_name="Slug")
    activa = models.BooleanField(default=True, verbose_name="¿Activa?")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """Genera el slug automáticamente si no existe."""
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class Producto(models.Model):
    """
    Modelo que representa un producto del ecommerce.

    Almacena toda la información de los productos incluyendo
    precio, stock, descripción y categoría.

    Atributos:
        nombre: Nombre del producto
        descripcion: Descripción detallada
        categoria: Relación con la categoría
        precio: Precio en moneda local
        precio_descuento: Precio con descuento (opcional)
        stock: Cantidad disponible
        imagen: Imagen principal del producto
        activo: Indica si el producto está activo
        destacado: Marca si es producto destacado
        slug: Identificador amigable para URLs
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(verbose_name="Descripción del producto")
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="productos",
        verbose_name="Categoría",
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Precio",
    )
    precio_descuento = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Precio con descuento",
    )
    stock = models.IntegerField(
        default=0, validators=[MinValueValidator(0)], verbose_name="Stock disponible"
    )
    imagen = models.ImageField(
        upload_to="productos/", verbose_name="Imagen del producto"
    )
    activo = models.BooleanField(default=True, verbose_name="¿Producto activo?")
    destacado = models.BooleanField(default=False, verbose_name="¿Producto destacado?")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["activo", "categoria"]),
        ]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        """Genera el slug automáticamente si no existe."""
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    @property
    def precio_final(self):
        """Retorna el precio final considerando descuentos."""
        if self.precio_descuento:
            return self.precio_descuento
        return self.precio

    @property
    def tiene_descuento(self):
        """Retorna True si el producto tiene descuento aplicado."""
        return self.precio_descuento is not None

    @property
    def porcentaje_descuento(self):
        """Calcula el porcentaje de descuento."""
        if self.tiene_descuento:
            descuento = self.precio - self.precio_descuento
            return (descuento / self.precio) * 100
        return 0

    def reducir_stock(self, cantidad):
        """
        Reduce el stock del producto.

        Args:
            cantidad: Cantidad a reducir

        Raises:
            ValueError: Si la cantidad es mayor al stock disponible
        """
        if cantidad > self.stock:
            raise ValueError(
                f"Stock insuficiente. Disponible: {self.stock}, Solicitado: {cantidad}"
            )
        self.stock -= cantidad
        self.save()

    def aumentar_stock(self, cantidad):
        """
        Aumenta el stock del producto.

        Args:
            cantidad: Cantidad a aumentar
        """
        self.stock += cantidad
        self.save()

    def en_stock(self):
        """Retorna True si el producto está en stock."""
        return self.stock > 0


class Imagen(models.Model):
    """
    Modelo para galería de imágenes de productos.

    Permite agregar múltiples imágenes a cada producto.

    Atributos:
        producto: Relación con el producto
        imagen: Archivo de imagen
        orden: Orden de visualización
        created_at: Fecha de creación
    """

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="galeria",
        verbose_name="Producto",
    )
    imagen = models.ImageField(upload_to="productos/galeria/", verbose_name="Imagen")
    orden = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Imagen"
        verbose_name_plural = "Imágenes"
        ordering = ["orden"]

    def __str__(self):
        return f"Imagen - {self.producto.nombre}"
