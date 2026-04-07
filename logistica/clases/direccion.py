from geopy.exc import GeocoderTimedOut
from geopy.geocoders import Nominatim


class Direccion:

    def __init__(self, pais, provincia, ciudad, calle, numero):

        self._pais = pais
        self._provincia = provincia
        self._ciudad = ciudad
        self._calle = calle
        self._numero = numero

        self.__coordenadas = None

        self._geolocator = Nominatim(user_agent="logistica_app")

    # ==========================
    # GETTERS (NECESARIOS)
    # ==========================

    @property
    def pais(self):
        return self._pais

    @property
    def provincia(self):
        return self._provincia

    @property
    def ciudad(self):
        return self._ciudad

    @property
    def calle(self):
        return self._calle

    @property
    def numero(self):
        return self._numero

    @property
    def coordenadas(self):
        return self.__coordenadas

    @coordenadas.setter
    def coordenadas(self, valor):
        self.__coordenadas = valor

    # ==========================
    # FUNCIONES
    # ==========================

    def direccion_completa(self):
        return f"{self._calle} {self._numero}, {self._ciudad}, {self._provincia}, {self._pais}"

    def validar(self):
        try:
            direccion = self.direccion_completa()
            location = self._geolocator.geocode(direccion, exactly_one=True)

            if location is None:
                return None

            if str(self._numero) not in location.address:
                return None

            return True

        except GeocoderTimedOut:
            return None

    def obtener_coordenadas(self):
        try:
            direccion = self.direccion_completa()
            location = self._geolocator.geocode(direccion, exactly_one=True)

            if location is None:
                return None

            self.__coordenadas = (location.latitude, location.longitude)
            return self.__coordenadas

        except GeocoderTimedOut:
            return None

    def __str__(self):

        if self.__coordenadas is None:
            return f"{self.direccion_completa()} (sin coordenadas)"

        return f"{self.direccion_completa()} -> {self.__coordenadas}"
