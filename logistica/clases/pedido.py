import random
from datetime import datetime
from exceptions.errores import PlazoInvalidoError, DireccionInvalidaError
from datos.ciudades import CIUDADES


class Pedido:

    def __init__(self, id, origen, destino, peso, volumen, fecha_entrega, nivel_servicio):

        self.id = id
        self.origen = origen
        self.destino = destino
        self.peso = peso
        self.volumen = volumen
        self.fecha_entrega = fecha_entrega
        self.nivel_servicio = nivel_servicio

        self.validar()

        # coordenadas simuladas (para mapas internos)
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)

        # coordenadas reales de la ciudad
        self.lat, self.lon = CIUDADES[origen]

    def validar(self):

        if not self.origen or not self.destino:
            raise DireccionInvalidaError("Dirección inválida")

        if self.fecha_entrega < datetime.now():
            raise PlazoInvalidoError("Fecha de entrega inválida")

    def coordenadas_origen(self):
        return CIUDADES[self.origen]

    def coordenadas_destino(self):
        return CIUDADES[self.destino]

    def __add__(self, other):

        nuevo_peso = self.peso + other.peso
        nuevo_volumen = self.volumen + other.volumen

        return Pedido(
            f"{self.id}-{other.id}",
            self.origen,
            other.destino,
            nuevo_peso,
            nuevo_volumen,
            self.fecha_entrega,
            self.nivel_servicio
        )

    def __str__(self):

        return f"Pedido:{self.id} {self.origen} → {self.destino} Peso:{self.peso} kg Vol:{self.volumen} l. Entrega:{self.fecha_entrega.date()} Hora:{self.fecha_entrega.strftime('%H:%M')} Servicio:{self.nivel_servicio}"