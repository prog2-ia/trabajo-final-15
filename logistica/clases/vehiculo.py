"""
==========================================================
MÓDULO: vehiculo.py
==========================================================

Jerarquía de vehículos del sistema logístico.

TIPOS:
✔ Camión
✔ Furgoneta
✔ Motocicleta
✔ Mochila

FUNCIONALIDADES:
✔ Validación de matrículas
✔ Control de disponibilidad
✔ Asociación a delegación
✔ Control de carga máxima
✔ Control de cubicaje
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC

from utiles.utils import validar_matricula_esp


# ==========================================================
# CLASE BASE VEHÍCULO
# ==========================================================
class Vehiculo(ABC):

    # ======================================================
    # REGISTROS
    # ======================================================
    _vehiculos = []

    matriculas_existentes = set()

    # ======================================================
    # CONSTRUCTOR
    # ======================================================
    def __init__(
            self,
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
    ):

        self.validar_matricula_unica(
            matricula
        )

        self._matricula = (
            matricula.upper()
        )

        self._disponible = (
            disponible
        )

        self._delegacion = (
            delegacion
        )

        self._carga_maxima = (
            carga_maxima
        )

        self._cubicaje = (
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
            matricula
    ):

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
    def matricula(self):
        return self._matricula

    @property
    def disponible(self):
        return self._disponible

    @property
    def delegacion(self):
        return self._delegacion

    @property
    def carga_maxima(self):
        return self._carga_maxima

    @property
    def cubicaje(self):
        return self._cubicaje

    # ======================================================
    # SETTERS
    # ======================================================
    @disponible.setter
    def disponible(
            self,
            valor
    ):
        self._disponible = valor

    # ======================================================
    # STR
    # ======================================================
    def __str__(self):

        return (
            f"{self.tipo.upper()} | "
            f"{self.matricula} | "
            f"Carga: {self.carga_maxima} | "
            f"Cubicaje: {self.cubicaje} | "
            f"{self.delegacion.nombre}"
        )


# ==========================================================
# CAMIÓN
# ==========================================================
class VehiculoCamion(Vehiculo):

    tipo = "camion"

    def __init__(
            self,
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
    ):

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
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
    ):

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
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
    ):

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
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
    ):

        super().__init__(
            matricula,
            disponible,
            delegacion,
            carga_maxima,
            cubicaje
        )