"""
EJERCICIO 3 — Figuras sin modificar la función

Crea las clases necesarias para que la función anterior funcione con:
● Rectangulo;
● Circulo;
● TrianguloRectangulo.
No puedes modificar imprimir_informe().
Cada figura debe implementar:
● nombre()
● area()
● perimetro()
Después añade una nueva figura Cuadrado intentando duplicar la menor cantidad posible de código.

"""

import math


class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def nombre(self):
        return "Rectángulo"

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def nombre(self):
        return "Círculo"

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio


class TrianguloRectangulo:
    def __init__(self, cateto_a, cateto_b):
        self.cateto_a = cateto_a
        self.cateto_b = cateto_b

    def nombre(self):
        return "Triángulo rectángulo"

    def area(self):
        return (self.cateto_a * self.cateto_b) / 2

    def perimetro(self):
        hipotenusa = math.sqrt(
            self.cateto_a ** 2 + self.cateto_b ** 2
        )
        return self.cateto_a + self.cateto_b + hipotenusa


class Cuadrado(Rectangulo):
    def __init__(self, lado):
        # Reutilizamos el constructor de Rectangulo.
        super().__init__(lado, lado)

    def nombre(self):
        return "Cuadrado"


# Esta función NO se modifica.
def imprimir_informe(figuras):
    for figura in figuras:
        print(
            figura.nombre(),
            round(figura.area(), 2),
            round(figura.perimetro(), 2)
        )


figuras = [
    Rectangulo(5, 3),
    Circulo(2),
    TrianguloRectangulo(3, 4),
    Cuadrado(4),
]

imprimir_informe(figuras)

# Resultado esperado aproximado:
# Rectángulo 15 16
# Círculo 12.57 12.57
# Triángulo rectángulo 6 12
# Cuadrado 16 16
