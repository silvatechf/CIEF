"""
EJERCICIO 5 — Refactorización

Este diseño obliga a modificar Pedido cada vez que aparece un nuevo tipo de cliente.
Refactoriza el programa utilizando POO para que sea posible crear nuevos tipos de descuento sin modificar la clase
que calcula el pedido.
Implementa al menos:
● cliente normal;
● cliente VIP;
● empleado;
● cliente premium.
Después añade:
● ClienteEstudiante → 15% de descuento
sin modificar la lógica principal de Pedido.


"""


class Descuento:
    def calcular(self, precio, cantidad):
        return precio * cantidad


class ClienteNormal(Descuento):
    pass


class ClienteVIP(Descuento):
    def calcular(self, precio, cantidad):
        return precio * cantidad * 0.8


class Empleado(Descuento):
    def calcular(self, precio, cantidad):
        return precio * cantidad * 0.5


class ClientePremium(Descuento):
    def calcular(self, precio, cantidad):
        return precio * cantidad * 0.7


class ClienteEstudiante(Descuento):
    def calcular(self, precio, cantidad):
        # 15% de descuento => se paga el 85%.
        return precio * cantidad * 0.85


class Pedido:
    def __init__(self, precio, cantidad, descuento):
        self.precio = precio
        self.cantidad = cantidad
        self.descuento = descuento

    def calcular_precio(self):
        # No hay if/elif según el tipo de cliente.
        return self.descuento.calcular(self.precio, self.cantidad)


# Comprobación de los cinco tipos.
clientes = [
    ("Normal", ClienteNormal()),
    ("VIP", ClienteVIP()),
    ("Empleado", Empleado()),
    ("Premium", ClientePremium()),
    ("Estudiante", ClienteEstudiante()),
]

for nombre, descuento in clientes:
    pedido = Pedido(100, 2, descuento)
    print(nombre, ":", pedido.calcular_precio())

# Resultado esperado:
# Normal: 200
# VIP: 160
# Empleado: 100
# Premium: 140
# Estudiante: 170
