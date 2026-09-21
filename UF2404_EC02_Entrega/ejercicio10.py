"""
EJERCICIO 10 — Sistema extensible de pedidos

Una tienda gestiona pedidos con distintos tipos de productos.
Existen inicialmente:
● ProductoFisico
● ProductoDigital
● Suscripcion
Todos comparten:
● id
● nombre
● precio_base
pero calculan su precio final de forma distinta.
Producto físico
● precio_base + coste_envio
Producto digital
● precio_base

Suscripción
Recibe además el número de meses:
● precio_base * meses
Crea también una clase Pedido.
Debe permitir:
● agregar(producto)
● eliminar(id_producto)
● calcular_total()
Añade estas condiciones:
● un pedido no puede contener dos productos con el mismo id;
● todos los precios deben ser válidos;
● calcular_total() no debe preguntar qué clase de producto está procesando mediante if type(...);
● el pedido debe seguir funcionando sin modificaciones si aparece un nuevo tipo de producto compatible.
Finalmente crea:
● ProductoDescuento
que recibe un porcentaje de descuento.
Intégralo en el pedido sin modificar calcular_total().
Segunda parte
El profesor indicará durante el examen un cambio no anunciado que el alumno deberá incorporar sin rediseñar
completamente la aplicación.
Posibles ejemplos:
● - IVA diferente según el producto.
● - Cantidades.
● - Envío gratuito a partir de determinado importe.
● - Nuevo tipo de producto.
● - Aplicación de un cupón.

"""


class Producto:
    def __init__(self, id_producto, nombre, precio_base):
        if precio_base < 0:
            raise ValueError("El precio base debe ser válido.")

        self.id = id_producto
        self.nombre = nombre
        self.precio_base = precio_base

    def precio_final(self):
        return self.precio_base


class ProductoFisico(Producto):
    def __init__(self, id_producto, nombre, precio_base, coste_envio):
        super().__init__(id_producto, nombre, precio_base)

        if coste_envio < 0:
            raise ValueError("El coste de envío debe ser válido.")

        self.coste_envio = coste_envio

    def precio_final(self):
        return self.precio_base + self.coste_envio


class ProductoDigital(Producto):
    def precio_final(self):
        return self.precio_base


class Suscripcion(Producto):
    def __init__(self, id_producto, nombre, precio_base, meses):
        super().__init__(id_producto, nombre, precio_base)

        if meses <= 0:
            raise ValueError("Los meses deben ser mayores que cero.")

        self.meses = meses

    def precio_final(self):
        return self.precio_base * self.meses


class ProductoDescuento(Producto):
    def __init__(
        self,
        id_producto,
        nombre,
        precio_base,
        porcentaje_descuento
    ):
        super().__init__(id_producto, nombre, precio_base)

        if not 0 <= porcentaje_descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

        self.porcentaje_descuento = porcentaje_descuento

    def precio_final(self):
        return (
            self.precio_base
            * (1 - self.porcentaje_descuento / 100)
        )


class Pedido:
    def __init__(self):
        self._productos = {}

    def agregar(self, producto):
        if producto.id in self._productos:
            raise ValueError("El pedido ya contiene ese producto.")

        self._productos[producto.id] = producto

    def eliminar(self, id_producto):
        if id_producto not in self._productos:
            raise ValueError("El producto no existe.")

        del self._productos[id_producto]

    def calcular_total(self):
        # No pregunta qué tipo de producto es.
        return sum(
            producto.precio_final()
            for producto in self._productos.values()
        )


# Comprobación de los tipos solicitados y de ProductoDescuento.
pedido = Pedido()

pedido.agregar(
    ProductoFisico("P1", "Teclado", 50, 5)
)
pedido.agregar(
    ProductoDigital("P2", "Curso Python", 80)
)
pedido.agregar(
    Suscripcion("P3", "Plataforma", 10, 3)
)
pedido.agregar(
    ProductoDescuento("P4", "Libro", 40, 15)
)

print("Total del pedido:", pedido.calcular_total())

# Resultado esperado:
# P1 = 50 + 5 = 55
# P2 = 80
# P3 = 10 * 3 = 30
# P4 = 40 - 15% = 34
# Total = 199
#
# ProductoDescuento se integra sin modificar calcular_total().
