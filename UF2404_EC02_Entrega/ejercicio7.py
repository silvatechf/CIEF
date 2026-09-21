"""
EJERCICIO 7 — Clases que deben funcionar juntas

Implementa un sistema de cursos.
Crea:
● Persona
● Alumno
● Profesor
● Curso
Alumno y Profesor deben heredar de Persona.
Un Curso tiene:
● un nombre;
● un profesor;
● varios alumnos;
● una capacidad máxima.
Debe permitir:
● matricular(alumno)
● desmatricular(alumno)
● cambiar_profesor(profesor)
Condiciones:
● únicamente pueden matricularse objetos Alumno;
● solamente un Profesor puede ser profesor del curso;
● un alumno no puede matricularse dos veces;
● debe respetarse la capacidad máxima.
Implementa también __str__() para mostrar un curso de forma legible.

"""


class Persona:
    def __init__(self, nombre):
        self.nombre = nombre


class Alumno(Persona):
    pass


class Profesor(Persona):
    pass


class Curso:
    def __init__(self, nombre, profesor, capacidad_maxima):
        if not isinstance(profesor, Profesor):
            raise TypeError("El profesor debe ser un objeto Profesor.")

        self.nombre = nombre
        self.profesor = profesor
        self._alumnos = []
        self.capacidad_maxima = capacidad_maxima

    def matricular(self, alumno):
        if not isinstance(alumno, Alumno):
            raise TypeError("Solo se pueden matricular alumnos.")

        if alumno in self._alumnos:
            raise ValueError("El alumno ya está matriculado.")

        if len(self._alumnos) >= self.capacidad_maxima:
            raise ValueError("Se ha alcanzado la capacidad máxima.")

        self._alumnos.append(alumno)

    def desmatricular(self, alumno):
        if alumno not in self._alumnos:
            raise ValueError("El alumno no está matriculado.")

        self._alumnos.remove(alumno)

    def cambiar_profesor(self, profesor):
        if not isinstance(profesor, Profesor):
            raise TypeError("Solo un Profesor puede ser profesor.")

        self.profesor = profesor

    def __str__(self):
        alumnos = ", ".join(
            alumno.nombre for alumno in self._alumnos
        )

        return (
            f"Curso: {self.nombre} | "
            f"Profesor: {self.profesor.nombre} | "
            f"Alumnos: {alumnos}"
        )


# Comprobación.
profesor = Profesor("Laura")
curso = Curso("Programación Orientada a Objetos", profesor, 2)

curso.matricular(Alumno("Ana"))
curso.matricular(Alumno("Marc"))

print(curso)

# Resultado esperado:
# Curso: Programación Orientada a Objetos |
# Profesor: Laura |
# Alumnos: Ana, Marc
