"""
==========================================================
MÓDULO: vehiculo.py
==========================================================

Jerarquía de vehículos del sistema logístico.
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC
from typing import List, Set

from utiles.utils import validar_matricula_esp


# ==========================================================
# CLASE BASE VEHÍCULO
# ==========================================================
class Vehiculo(ABC):

    tipo: str = "vehiculo"

    # ======================================================
    # REGISTROS
    # ======================================================
    _vehiculos: List["Vehiculo"] = []

    matriculas_existentes: Set[str] = set()

    # ======================================================
    # VEHÍCULOS REGISTRADOS
    # ======================================================
    @classmethod
    def vehiculos_registrados(cls) -> List["Vehiculo"]:
        return cls._vehiculos

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    def __init__(
            self,
            matricula: str,
            disponible: bool,
            delegacion,
            carga_maxima: float,
            cubicaje: float
    ) -> None:

        self.validar_matricula_unica(
            matricula
        )

        self._matricula: str = (
            matricula.upper()
        )

        self._disponible: bool = (
            disponible
        )

        self._delegacion = (
            delegacion
        )

        self._carga_maxima: float = (
            carga_maxima
        )

        self._cubicaje: float = (
            cubicaje
        )

        Vehiculo.matriculas_existentes.add(
            self._matricula
        )

        Vehiculo._vehiculos.append(self)

    # ======================================================
    # VALIDAR MATRÍCULA ÚNICA
    # ======================================================
    @classmethod
    def validar_matricula_unica(
            cls,
            matricula: str
    ) -> None:

        if (
                matricula.upper()
                in cls.matriculas_existentes
        ):

            raise ValueError(
                "La matrícula ya existe"
            )

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def matricula(self) -> str:
        return self._matricula

    @property
    def disponible(self) -> bool:
        return self._disponible

    @property
    def delegacion(self):
        return self._delegacion

    @property
    def carga_maxima(self) -> float:
        return self._carga_maxima

    @property
    def cubicaje(self) -> float:
        return self._cubicaje

    # ======================================================
    # SET DISPONIBLE
    # ======================================================
    def set_disponible(
            self,
            valor: bool
    ) -> None:

        self._disponible = valor

    # ======================================================
    # MÉTODOS
    # ======================================================
    def asignar_delegacion(
            self,
            delegacion
    ) -> None:

        self._delegacion = delegacion

    def quitar_delegacion(self) -> None:

        self._delegacion = None

    # ======================================================
    # STR
    # ======================================================
    def __str__(self) -> str:

        nombre_delegacion = (
            self.delegacion.nombre
            if self.delegacion
            else "SIN DELEGACIÓN"
        )

        return (
            f"{self.tipo.upper()} | "
            f"{self.matricula} | "
            f"Carga: {self.carga_maxima} | "
            f"Cubicaje: {self.cubicaje} | "
            f"{nombre_delegacion}"
        )


# ==========================================================
# CAMIÓN
# ==========================================================
class VehiculoCamion(Vehiculo):

    tipo = "camion"

    def __init__(
            self,
            matricula: str,
            disponible: bool,
            delegacion,
            carga_maxima: float,
            cubicaje: float
    ) -> None:

        if not validar_matricula_esp(
                matricula
        ):

            raise ValueError(
                "Matrícula inválida"
            )

        super().__init__(
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
        )


# ==========================================================
# FURGONETA
# ==========================================================
class VehiculoFurgoneta(Vehiculo):

    tipo = "furgoneta"

    def __init__(
            self,
            matricula: str,
            disponible: bool,
            delegacion,
            carga_maxima: float,
            cubicaje: float
    ) -> None:

        if not validar_matricula_esp(
                matricula
        ):

            raise ValueError(
                "Matrícula inválida"
            )

        super().__init__(
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
        )


# ==========================================================
# MOTOCICLETA
# ==========================================================
class VehiculoMotocicleta(Vehiculo):

    tipo = "motocicleta"

    def __init__(
            self,
            matricula: str,
            disponible: bool,
            delegacion,
            carga_maxima: float,
            cubicaje: float
    ) -> None:

        if not validar_matricula_esp(
                matricula
        ):

            raise ValueError(
                "Matrícula inválida"
            )

        super().__init__(
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
        )


# ==========================================================
# MOCHILA
# ==========================================================
class VehiculoMochila(Vehiculo):

    tipo = "mochila"

    def __init__(
            self,
            matricula: str,
            disponible: bool,
            delegacion,
            carga_maxima: float,
            cubicaje: float
    ) -> None:

        super().__init__(
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
        )