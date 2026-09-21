"""
EJERCICIO 9 — Sistema de préstamos

Crea un sistema de biblioteca con:
● Libro
● Usuario
● Prestamo
● Biblioteca
Un libro puede estar disponible o prestado.La biblioteca debe permitir:
● agregar_libro(libro)
● registrar_usuario(usuario)
● prestar(isbn, id_usuario)
● devolver(isbn)
● prestamos_activos()
Condiciones:
● cada libro debe tener un ISBN único;
● cada usuario debe tener un identificador único;
● no puede prestarse un libro que ya esté prestado;
● cada usuario puede tener como máximo 3 libros simultáneamente;
● un Prestamo debe relacionar un libro y un usuario;
● devolver un libro debe finalizar el préstamo correspondiente.
No almacenes simplemente nombres o ISBN dentro de Prestamo: utiliza objetos

"""


class Libro:
    def __init__(self, isbn, titulo):
        self.isbn = isbn
        self.titulo = titulo
        self.disponible = True


class Usuario:
    def __init__(self, id_usuario, nombre):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self._prestamos = []

    def numero_prestamos(self):
        return len(self._prestamos)


class Prestamo:
    def __init__(self, libro, usuario):
        # Se guardan los objetos completos.
        self.libro = libro
        self.usuario = usuario
        self.activo = True

    def finalizar(self):
        self.activo = False


class Biblioteca:
    def __init__(self):
        self._libros = {}
        self._usuarios = {}
        self._prestamos = []

    def agregar_libro(self, libro):
        if libro.isbn in self._libros:
            raise ValueError("El ISBN ya existe.")

        self._libros[libro.isbn] = libro

    def registrar_usuario(self, usuario):
        if usuario.id_usuario in self._usuarios:
            raise ValueError("El identificador ya existe.")

        self._usuarios[usuario.id_usuario] = usuario

    def prestar(self, isbn, id_usuario):
        if isbn not in self._libros:
            raise ValueError("El libro no existe.")

        if id_usuario not in self._usuarios:
            raise ValueError("El usuario no existe.")

        libro = self._libros[isbn]
        usuario = self._usuarios[id_usuario]

        if not libro.disponible:
            raise ValueError("El libro ya está prestado.")

        if usuario.numero_prestamos() >= 3:
            raise ValueError("El usuario ya tiene 3 libros prestados.")

        prestamo = Prestamo(libro, usuario)

        libro.disponible = False
        usuario._prestamos.append(prestamo)
        self._prestamos.append(prestamo)

    def devolver(self, isbn):
        for prestamo in self._prestamos:
            if prestamo.libro.isbn == isbn and prestamo.activo:
                prestamo.finalizar()
                prestamo.libro.disponible = True
                prestamo.usuario._prestamos.remove(prestamo)
                return

        raise ValueError("No existe un préstamo activo para ese libro.")

    def prestamos_activos(self):
        return [
            prestamo
            for prestamo in self._prestamos
            if prestamo.activo
        ]


# Comprobación.
biblioteca = Biblioteca()

libro = Libro("ISBN001", "Python")
usuario = Usuario("U001", "Ana")

biblioteca.agregar_libro(libro)
biblioteca.registrar_usuario(usuario)

biblioteca.prestar("ISBN001", "U001")

print("Préstamos activos:", len(biblioteca.prestamos_activos()))
print("Libro disponible:", libro.disponible)

biblioteca.devolver("ISBN001")

print("Préstamos activos después de devolver:",
      len(biblioteca.prestamos_activos()))
print("Libro disponible:", libro.disponible)

# Resultado esperado:
# Préstamos activos: 1
# Libro disponible: False
# Préstamos activos después de devolver: 0
# Libro disponible: True
