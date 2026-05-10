"""
Clase abstracta Delegacion.

Los vehículos conocen directamente su delegación.
La delegación puede consultar sus vehículos asociados.
"""

from abc import ABC, abstractmethod

from utiles.geolocalizacion import geocodificar


class Delegacion(ABC):

    nombres_registrados = set()

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(
            self,
            nombre,
            direccion,
            delegacion_superior=None,
            provincia=None,
            poblacion=None,
            coordenadas=None
    ):

        self.validar_nombre(nombre)

        self._nombre = nombre
        self._direccion = direccion

        self._delegacion_superior = delegacion_superior

        self._provincia = provincia
        self._poblacion = poblacion

        self._coordenadas = coordenadas

        Delegacion.nombres_registrados.add(nombre)

    # ======================================================
    # PROPIEDADES
    # ======================================================

    @property
    def nombre(self):
        return self._nombre

    @property
    def direccion(self):
        return self._direccion

    @property
    def coordenadas(self):
        return self._coordenadas

    @property
    def provincia(self):
        return self._provincia

    @property
    def poblacion(self):
        return self._poblacion

    @property
    def delegacion_superior(self):
        return self._delegacion_superior

    @property
    def vehiculos(self):
        """
        Retorna todos los vehículos asignados
        a esta delegación.
        """

        from clases.vehiculo import Vehiculo

        return [
            v for v in Vehiculo.vehiculos_registrados()
            if v.delegacion == self
        ]

    # ======================================================
    # VALIDACIONES
    # ======================================================

    @classmethod
    def validar_nombre(cls, nombre):

        if nombre in cls.nombres_registrados:
            raise ValueError(
                f"Ya existe una delegación con nombre '{nombre}'"
            )

    # ======================================================
    # GEOLOCALIZACIÓN
    # ======================================================

    def calcular_coordenadas(self):
        """
        Calcula coordenadas geográficas a partir
        de la dirección.
        """

        self._coordenadas = geocodificar(
            self._direccion
        )

    # ======================================================
    # GESTIÓN DE VEHÍCULOS
    # ======================================================

    def anadir_vehiculo(self, vehiculo):

        if not self.validar_vehiculo(vehiculo):
            raise ValueError(
                f"La delegación '{self.nombre}' no admite "
                f"vehículos tipo '{vehiculo.tipo}'"
            )

        vehiculo.asignar_delegacion(self)

    def quitar_vehiculo(self, vehiculo):

        if vehiculo.delegacion == self:
            vehiculo.quitar_delegacion()

    def vehiculos_disponibles(self):

        return [
            v for v in self.vehiculos
            if v.disponible
        ]

    # ======================================================
    # MÉTODOS ABSTRACTOS
    # ======================================================

    @abstractmethod
    def validar_vehiculo(self, vehiculo):
        pass

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================

    def __str__(self):

        return (
            f"{self.__class__.__name__}: "
            f"{self.nombre} | "
            f"{self.poblacion} | "
            f"{self.provincia}"
        )


# ==========================================================
# DELEGACIÓN CENTRAL
# ==========================================================

class DelegacionCentral(Delegacion):

    def validar_vehiculo(self, vehiculo):
        return vehiculo.tipo == "camion"


# ==========================================================
# DELEGACIÓN BASE
# ==========================================================

class DelegacionBase(Delegacion):

    def validar_vehiculo(self, vehiculo):
        return vehiculo.tipo == "furgoneta"


# ==========================================================
# DELEGACIÓN DESPACHO
# ==========================================================

class DelegacionDespacho(Delegacion):

    def validar_vehiculo(self, vehiculo):

        return vehiculo.tipo in [
            "furgoneta",
            "motocicleta",
            "mochila"
        ]