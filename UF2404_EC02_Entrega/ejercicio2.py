"""
EJERCICIO 2 — Reserva de plazas

Crea una clase Evento que represente un evento con un número máximo de plazas.
Debe permitir:
● reservar(persona)
● cancelar(persona)
● plazas_disponibles()
Condiciones:
● una persona no puede reservar dos veces;
● no pueden superarse las plazas disponibles;
● no puede cancelarse una reserva inexistente;
● la lista interna de personas inscritas no debe poder modificarse directamente desde fuera.
Además:
● len(evento)
debe devolver el número de personas inscritas.


"""


class Evento:
    def __init__(self, capacidad):
        self._capacidad = capacidad
        self._personas = []

    def reservar(self, persona):
        if persona in self._personas:
            raise ValueError("La persona ya tiene una reserva.")

        if len(self._personas) >= self._capacidad:
            raise ValueError("No quedan plazas disponibles.")

        self._personas.append(persona)

    def cancelar(self, persona):
        if persona not in self._personas:
            raise ValueError("La persona no tiene una reserva.")

        self._personas.remove(persona)

    def plazas_disponibles(self):
        return self._capacidad - len(self._personas)

    def personas_inscritas(self):
        # Se devuelve una copia, no la lista interna.
        return list(self._personas)

    def __len__(self):
        return len(self._personas)


# Comprobación.
evento = Evento(2)

evento.reservar("Ana")
evento.reservar("Marc")

print("Inscritos:", evento.personas_inscritas())
print("Plazas disponibles:", evento.plazas_disponibles())
print("Número de inscritos:", len(evento))

evento.cancelar("Marc")

print("Después de cancelar:", evento.personas_inscritas())

# Resultado esperado:
# Inscritos: ['Ana', 'Marc']
# Plazas disponibles: 0
# Número de inscritos: 2
# Después de cancelar: ['Ana']
