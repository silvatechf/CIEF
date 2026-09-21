"""
EJERCICIO 1 — Reparar un diseño defectuoso

El programa contiene varios errores, algunos de ejecución y otros relacionados con el diseño orientado a objetos.
Debes:
1. identificar al menos 4 problemas;
2. corregirlos;
3. explicar brevemente por qué es necesario cada cambio;
4. conseguir que cada usuario tenga su propia lista de cursos;
5. conseguir que Usuario.total indique correctamente cuántos usuarios se han creado.

"""


class Usuario:
    total = 0

    def __init__(self, nombre, cursos=None):
        self.nombre = nombre

        # Corrección de los problemas 1 y 2:
        # cada Usuario obtiene una lista independiente.
        self.cursos = [] if cursos is None else list(cursos)

        # Corrección de los problemas 4 y 5:
        # total es un atributo de clase.
        Usuario.total += 1

    def agregar_curso(self, curso):
        # Corrección del problema 3:
        # se modifica la lista perteneciente a este objeto.
        self.cursos.append(curso)


# Comprobación solicitada por el ejercicio.
u1 = Usuario("Ana")
u2 = Usuario("Marc")

u1.agregar_curso("Python")

print("Cursos de Ana:", u1.cursos)
print("Cursos de Marc:", u2.cursos)
print("Total de usuarios:", Usuario.total)

# Resultado esperado:
# Cursos de Ana: ['Python']
# Cursos de Marc: []
# Total de usuarios: 2
