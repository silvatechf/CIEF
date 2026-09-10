"""
Tests para la aplicación de Productos.

Documentación: https://docs.djangoproject.com/es/5.0/topics/testing/
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Categoria, Producto


class CategoriaTestCase(TestCase):
    """Tests para el modelo Categoria."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.categoria = Categoria.objects.create(
            nombre="Electrónica", descripcion="Productos electrónicos", activa=True
        )

    def test_crear_categoria(self):
        """Test: Crear una categoría."""
        self.assertEqual(self.categoria.nombre, "Electrónica")
        self.assertTrue(self.categoria.activa)

    def test_slug_auto_generado(self):
        """Test: El slug se genera automáticamente."""
        self.assertEqual(self.categoria.slug, "electronica")

    def test_str_categoria(self):
        """Test: Representación en string."""
        self.assertEqual(str(self.categoria), "Electrónica")


class ProductoTestCase(TestCase):
    """Tests para el modelo Producto."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.categoria = Categoria.objects.create(nombre="Laptops", activa=True)
        self.producto = Producto.objects.create(
            nombre="Laptop Dell XPS",
            descripcion="Laptop de alta gama",
            categoria=self.categoria,
            precio=1500.00,
            precio_descuento=1200.00,
            stock=10,
            activo=True,
        )

    def test_crear_producto(self):
        """Test: Crear un producto."""
        self.assertEqual(self.producto.nombre, "Laptop Dell XPS")
        self.assertEqual(self.producto.stock, 10)

    def test_precio_final_con_descuento(self):
        """Test: Calcular precio final con descuento."""
        self.assertEqual(self.producto.precio_final, 1200.00)

    def test_tiene_descuento(self):
        """Test: Verificar si tiene descuento."""
        self.assertTrue(self.producto.tiene_descuento)

    def test_porcentaje_descuento(self):
        """Test: Calcular porcentaje de descuento."""
        descuento_esperado = 20.0  # 20% de descuento
        self.assertEqual(self.producto.porcentaje_descuento, descuento_esperado)

    def test_reducir_stock(self):
        """Test: Reducir stock."""
        self.producto.reducir_stock(3)
        self.assertEqual(self.producto.stock, 7)

    def test_aumentar_stock(self):
        """Test: Aumentar stock."""
        self.producto.aumentar_stock(5)
        self.assertEqual(self.producto.stock, 15)

    def test_reducir_stock_insuficiente(self):
        """Test: Error al reducir más de lo disponible."""
        with self.assertRaises(ValueError):
            self.producto.reducir_stock(20)

    def test_en_stock(self):
        """Test: Verificar si está en stock."""
        self.assertTrue(self.producto.en_stock())
        self.producto.stock = 0
        self.producto.save()
        self.assertFalse(self.producto.en_stock())


class ProductoViewsTestCase(TestCase):
    """Tests para las vistas de Productos."""

    def setUp(self):
        """Configuración inicial para cada test."""
        self.client = Client()
        self.categoria = Categoria.objects.create(nombre="Celulares", activa=True)
        self.producto = Producto.objects.create(
            nombre="iPhone 15",
            descripcion="Último modelo",
            categoria=self.categoria,
            precio=1000.00,
            stock=5,
            activo=True,
        )

    def test_listar_productos_view(self):
        """Test: Vista de listado de productos."""
        response = self.client.get("/productos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone 15")

    def test_detalle_producto_view(self):
        """Test: Vista de detalles del producto."""
        response = self.client.get(f"/productos/{self.producto.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "iPhone 15")

    def test_producto_inactivo_no_visible(self):
        """Test: Producto inactivo no aparece en listado."""
        self.producto.activo = False
        self.producto.save()
        response = self.client.get("/productos/")
        self.assertNotContains(response, "iPhone 15")
