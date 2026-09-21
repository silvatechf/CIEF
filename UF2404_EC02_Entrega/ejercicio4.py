"""
EJERCICIO 4 — Historial bancario

Crea una clase CuentaBancaria.
Debe permitir:
● ingresar(cantidad)
● retirar(cantidad)
● transferir(cuenta_destino, cantidad)
Cada operación debe quedar almacenada en un historial.
Condiciones:
● no se permiten cantidades negativas o cero;
● no se puede retirar más dinero del disponible;
● una transferencia debe modificar correctamente ambas cuentas;
● el historial devuelto al usuario no debe permitir modificar el historial interno real.
Implementa:
● obtener_historial()

"""


class CuentaBancaria:
    def __init__(self, saldo=0):
        self._saldo = saldo
        self._historial = []

    @property
    def saldo(self):
        return self._saldo

    def ingresar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        self._saldo += cantidad
        self._historial.append(f"INGRESO +{cantidad}")

    def retirar(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self._saldo:
            raise ValueError("No se puede retirar más dinero del disponible.")

        self._saldo -= cantidad
        self._historial.append(f"RETIRADA -{cantidad}")

    def transferir(self, cuenta_destino, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")

        if cantidad > self._saldo:
            raise ValueError("No se puede transferir más dinero del disponible.")

        self._saldo -= cantidad
        cuenta_destino._saldo += cantidad

        self._historial.append(f"TRANSFERENCIA -{cantidad}")
        cuenta_destino._historial.append(f"TRANSFERENCIA +{cantidad}")

    def obtener_historial(self):
        # Copia para proteger el historial interno.
        return list(self._historial)


# Comprobación.
cuenta1 = CuentaBancaria(100)
cuenta2 = CuentaBancaria(50)

cuenta1.ingresar(100)
cuenta1.retirar(30)
cuenta1.transferir(cuenta2, 20)

print("Saldo cuenta 1:", cuenta1.saldo)
print("Saldo cuenta 2:", cuenta2.saldo)
print("Historial cuenta 1:", cuenta1.obtener_historial())

# Resultado esperado:
# Saldo cuenta 1: 150
# Saldo cuenta 2: 70
# Historial cuenta 1:
# ['INGRESO +100', 'RETIRADA -30', 'TRANSFERENCIA -20']
