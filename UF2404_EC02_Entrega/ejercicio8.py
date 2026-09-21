"""
EJERCICIO 8 


1. Escribe qué resultado crees que mostrará.
2. Explica por qué.
3. Ejecútalo y comprueba la respuesta.
4. Modifica únicamente el orden de herencia de D y explica cómo cambia el resultado.
5. Explica qué está haciendo realmente super() en este ejemplo.

"""


class A:
    def metodo(self):
        return "A"


class B(A):
    def metodo(self):
        return "B" + super().metodo()


class C(A):
    def metodo(self):
        return "C" + super().metodo()


class D(B, C):
    def metodo(self):
        return "D" + super().metodo()


# 1, 2 y 3: predicción, explicación y comprobación.
obj = D()

print("Resultado D:", obj.metodo())
print("MRO D:", D.mro())

# 4: únicamente cambiamos el orden de herencia.
class DInvertida(C, B):
    def metodo(self):
        return "D" + super().metodo()


obj_invertida = DInvertida()

print("Resultado DInvertida:", obj_invertida.metodo())
print("MRO DInvertida:", DInvertida.mro())

# Resultado esperado:
# Resultado D: DBCA
# Resultado DInvertida: DCBA
