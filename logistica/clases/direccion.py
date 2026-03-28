
"""
    CLASE DIRECCION

    Esta clase representa una direccion completa y permite:

    - Construir la direccion en formato texto
      metodo direccion_completa()

    - Validar si la direccion existe realmente
      metodo validar()

    - Obtener las coordenadas geograficas
      metodo obtener_coordenadas()

    - Acceder a las coordenadas
      propiedad coordenadas

    - Mostrar la direccion
      metodo __str__()

    ATRIBUTOS
    _pais, _provincia, _ciudad, _calle, _numero -> protegidos
    __coordenadas -> privado

    LIBRERIA
    geopy con Nominatim

    COMPORTAMIENTO
    No usa raise
    No usa print
    Devuelve None si hay errores
"""

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class Direccion:

    def __init__(self, pais, provincia, ciudad, calle, numero):

        # atributos protegidos
        self._pais = pais
        self._provincia = provincia
        self._ciudad = ciudad
        self._calle = calle
        self._numero = numero

        # atributo privado
        self.__coordenadas = None

        # geolocalizador
        self._geolocator = Nominatim(user_agent="logistica_app")

    # getter coordenadas
    @property
    def coordenadas(self):
        return self.__coordenadas

    # construye direccion completa
    def direccion_completa(self):
        return f"{self._calle} {self._numero}, {self._ciudad}, {self._provincia}, {self._pais}"

    # valida direccion
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

    # obtiene coordenadas
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

    # representacion en texto
    def __str__(self):

        if self.__coordenadas is None:
            return f"{self.direccion_completa()} (sin coordenadas)"

        return f"{self.direccion_completa()} -> {self.__coordenadas}"