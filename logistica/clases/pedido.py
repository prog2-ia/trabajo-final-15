import random
from datetime import datetime
import utiles.utils as utils
from logistica.datos.dic_ciudades_alicante import CIUDADES_ALICANTE


class Pedido:
    """
    Clase Pedido (versión silenciosa)
    - No usa raise
    - No usa print
    - Manejo de errores devolviendo None o ignorando cambios
    """

    def __init__(self, id, origen, destino, peso, volumen, fecha_entrega, nivel_servicio):

        self.id = id

        # Atributos protegidos
        self._origen = origen
        self._destino = destino
        self._peso = peso if peso > 0 else None
        self._volumen = volumen if volumen > 0 else None

        # Atributos privados
        self.__fecha_entrega = fecha_entrega if fecha_entrega >= datetime.now() else None
        self.__nivel_servicio = nivel_servicio if nivel_servicio in ["standard", "urgente"] else None

        # Coordenadas simuladas
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)

        # Coordenadas reales (o None si no existen)
        coords_origen = CIUDADES_ALICANTE.get(origen)
        coords_destino = CIUDADES_ALICANTE.get(destino)

        if coords_origen:
            self.lat, self.lon = coords_origen
        else:
            self.lat, self.lon = (None, None)

        if coords_destino:
            self.lat_des, self.lon_des = coords_destino
        else:
            self.lat_des, self.lon_des = (None, None)

        # Distancia
        self._km = self.calcular_distancia()

    # ==========================================
    # GETTERS Y SETTERS
    # ==========================================

    @property
    def origen(self):
        return self._origen

    @origen.setter
    def origen(self, valor):
        if valor in CIUDADES_ALICANTE:
            self._origen = valor

    @property
    def destino(self):
        return self._destino

    @destino.setter
    def destino(self, valor):
        if valor in CIUDADES_ALICANTE:
            self._destino = valor

    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if valor > 0:
            self._peso = valor
        else:
            return None

    @property
    def volumen(self):
        return self._volumen

    @volumen.setter
    def volumen(self, valor):
        if valor > 0:
            self._volumen = valor
        else:
            return None

    @property
    def fecha_entrega(self):
        return self.__fecha_entrega

    @fecha_entrega.setter
    def fecha_entrega(self, valor):
        if valor >= datetime.now():
            self.__fecha_entrega = valor
        else:
            return None

    @property
    def nivel_servicio(self):
        return self.__nivel_servicio

    @nivel_servicio.setter
    def nivel_servicio(self, valor):
        if valor in ["standard", "urgente"]:
            self.__nivel_servicio = valor
        else:
            return None

    @property
    def km(self):
        return self._km

    # ==========================================
    # MÉTODOS
    # ==========================================

    def coordenadas_origen(self):
        return CIUDADES_ALICANTE.get(self._origen)

    def coordenadas_destino(self):
        return CIUDADES_ALICANTE.get(self._destino)

    def calcular_distancia(self):
        if None in (self.lat, self.lon, self.lat_des, self.lon_des):
            return None

        return utils.distancia_km(
            (self.lat, self.lon),
            (self.lat_des, self.lon_des)
        )

    # ==========================================
    # POLIMORFISMO (OPERADOR +)
    # ==========================================

    def __add__(self, other):

        if not isinstance(other, Pedido):
            return None

        if self._peso is None or other._peso is None:
            return None

        if self._volumen is None or other._volumen is None:
            return None

        return Pedido(
            f"{self.id}-{other.id}",
            self._origen,
            other._destino,
            self._peso + other._peso,
            self._volumen + other._volumen,
            self.__fecha_entrega if self.__fecha_entrega else datetime.now(),
            self.__nivel_servicio if self.__nivel_servicio else "standard"
        )

    # ==========================================
    # REPRESENTACIÓN
    # ==========================================

    def __str__(self):

        if None in (self._peso, self._volumen, self.__fecha_entrega, self.__nivel_servicio, self._km):
            return "Pedido inválido"

        return (
            f"Pedido:{self.id} {self._origen} → {self._destino} "
            f"{self._km:.1f} km Peso:{self._peso} kg "
            f"Vol:{self._volumen} l. "
            f"Entrega:{self.__fecha_entrega.date()} "
            f"Hora:{self.__fecha_entrega.strftime('%H:%M')} "
            f"Servicio:{self.__nivel_servicio}"
        )