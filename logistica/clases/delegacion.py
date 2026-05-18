"""
==========================================================
MÓDULO: delegacion.py
==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC
from typing import List, Optional, Set, Tuple

from utiles.geolocalizacion import (
    geocodificar,
    obtener_datos_geo
)


# ==========================================================
# CLASE BASE DELEGACIÓN
# ==========================================================
class Delegacion(ABC):

    tipo: str = "delegacion"

    # ======================================================
    # REGISTRO GLOBAL
    # ======================================================
    nombres_registrados: Set[str] = set()

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    def __init__(
            self,
            nombre: str,
            direccion: str,
            superior=None,
            coordenadas: Optional[
                Tuple[float, float]
            ] = None,
            provincia_inicial: str = "",
            poblacion_inicial: str = ""
    ) -> None:

        self.validar_nombre(nombre)

        self._nombre: str = nombre

        self._direccion: str = direccion

        self._superior = superior

        self._vehiculos: List = []

        self._coordenadas: Optional[
            Tuple[float, float]
        ] = coordenadas

        # ==================================================
        # DATOS GEO
        # ==================================================
        self._provincia: str = provincia_inicial

        self._poblacion: str = poblacion_inicial

        # ==================================================
        # GEOLOCALIZACIÓN
        # ==================================================
        if self._coordenadas is None:

            self.calcular_coordenadas()

        # ==================================================
        # SOLO CALCULAR SI NO EXISTEN YA
        # ==================================================
        if self._coordenadas:

            if not self._poblacion or not self._provincia:

                poblacion_geo, provincia_geo = (
                    obtener_datos_geo(
                        self._coordenadas
                    )
                )

                if (
                        not self._poblacion
                        and poblacion_geo
                ):

                    self._poblacion = (
                        poblacion_geo
                    )

                if (
                        not self._provincia
                        and provincia_geo
                ):

                    self._provincia = (
                        provincia_geo
                    )

        Delegacion.nombres_registrados.add(
            nombre.upper()
        )

    # ======================================================
    # VALIDAR NOMBRE
    # ======================================================
    @classmethod
    def validar_nombre(
            cls,
            nombre: str
    ) -> None:

        if (
                nombre.upper()
                in cls.nombres_registrados
        ):

            raise ValueError(
                "Ya existe una delegación"
            )

    # ======================================================
    # GEOLOCALIZACIÓN
    # ======================================================
    def calcular_coordenadas(self) -> None:

        coordenadas = geocodificar(
            self._direccion
        )

        if coordenadas:

            self._coordenadas = coordenadas

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def superior(self):
        return self._superior

    @property
    def delegacion_superior(self):
        return self._superior

    @property
    def coordenadas(
            self
    ) -> Optional[Tuple[float, float]]:

        return self._coordenadas

    @property
    def provincia(self) -> str:
        return self._provincia

    @property
    def poblacion(self) -> str:
        return self._poblacion

    @property
    def vehiculos(self) -> List:
        return self._vehiculos

    # ======================================================
    # MÉTODOS SET
    # ======================================================
    def set_provincia(
            self,
            valor: str
    ) -> None:

        self._provincia = valor

    def set_poblacion(
            self,
            valor: str
    ) -> None:

        self._poblacion = valor
    """
    # ======================================================
    # SETTERS
    # ======================================================
    @provincia.setter
    def provincia(
            self,
            valor: str
    ) -> None:

        self._provincia = valor

    @poblacion.setter
    def poblacion(
            self,
            valor: str
    ) -> None:

        self._poblacion = valor
    """

    # ======================================================
    # SET DIRECCIÓN
    # ======================================================
    def set_direccion(
            self,
            nueva_direccion: str
    ) -> None:

        self._direccion = nueva_direccion

        self.calcular_coordenadas()

    # ======================================================
    # VEHÍCULOS
    # ======================================================
    def agregar_vehiculo(
            self,
            vehiculo
    ) -> None:

        if vehiculo not in self._vehiculos:

            self._vehiculos.append(
                vehiculo
            )

    def eliminar_vehiculo(
            self,
            vehiculo
    ) -> None:

        if vehiculo in self._vehiculos:

            self._vehiculos.remove(
                vehiculo
            )

    def vehiculos_disponibles(self) -> List:

        return [

            v for v in self._vehiculos

            if v.disponible
        ]

    # ======================================================
    # STR
    # ======================================================
    def __str__(self) -> str:

        return (
            f"{self.tipo.upper()} | "
            f"{self.nombre} | "
            f"{self.poblacion} | "
            f"{self.provincia}"
        )


# ==========================================================
# CENTRAL
# ==========================================================
class DelegacionCentral(Delegacion):

    tipo = "central"


# ==========================================================
# BASE
# ==========================================================
class DelegacionBase(Delegacion):

    tipo = "base"


# ==========================================================
# DESPACHO
# ==========================================================
class DelegacionDespacho(Delegacion):

    tipo = "despacho"