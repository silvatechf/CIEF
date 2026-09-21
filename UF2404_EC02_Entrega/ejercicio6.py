"""
EJERCICIO 6 — Sistema de inventario

Crea las clases necesarias para gestionar un inventario.
Cada Producto tiene:
● codigo
● nombre
● precio
● stock
El Inventario debe permitir:
● agregar_producto(producto)
● eliminar_producto(codigo)
● buscar(codigo)
● vender(codigo, cantidad)
● reponer(codigo, cantidad)
● valor_total()
Condiciones:
● dos productos no pueden tener el mismo código;
● no puede venderse más stock del disponible;
● precio, cantidad y stock deben ser válidos;
● valor_total() devuelve el valor monetario de todo el stock;
● la colección interna de productos no debe quedar expuesta directamente.


"""


class Producto:
    def __init__(self, codigo, nombre, precio, stock):
        if precio < 0:
            raise ValueError("El precio debe ser válido.")

        if stock < 0:
            raise ValueError("El stock debe ser válido.")

        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock = stock


class Inventario:
    def __init__(self):
        self._productos = {}

    def agregar_producto(self, producto):
        if producto.codigo in self._productos:
            raise ValueError("Ya existe un producto con ese código.")

        self._productos[producto.codigo] = producto

    def eliminar_producto(self, codigo):
        if codigo not in self._productos:
            raise ValueError("El producto no existe.")

        del self._productos[codigo]

    def buscar(self, codigo):
        if codigo not in self._productos:
            raise ValueError("El producto no existe.")

        return self._productos[codigo]

    def vender(self, codigo, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        producto = self.buscar(codigo)

        if cantidad > producto.stock:
            raise ValueError("No hay suficiente stock.")

        producto.stock -= cantidad

    def reponer(self, codigo, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        producto = self.buscar(codigo)
        producto.stock += cantidad

    def valor_total(self):
        return sum(
            producto.precio * producto.stock
            for producto in self._productos.values()
        )

    def productos(self):
        # Se devuelve una lista nueva, no el diccionario interno.
        return list(self._productos.values())


# Comprobación.
inventario = Inventario()

inventario.agregar_producto(
    Producto("P001", "Teclado", 25, 10)
)
inventario.agregar_producto(
    Producto("P002", "Ratón", 15, 20)
)

inventario.vender("P001", 2)
inventario.reponer("P002", 5)

print("Stock P001:", inventario.buscar("P001").stock)
print("Valor total:", inventario.valor_total())

# Resultado esperado:
# Stock P001: 8
# Valor total: 500
