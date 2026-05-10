"""
CLASES VEHÍCULO DEL SISTEMA LOGÍSTICO

Modelo refactorizado:
✔ Cada vehículo conoce directamente su delegación
✔ Las delegaciones ya NO almacenan flotas
✔ Relación:
    Delegacion 1 ---- * Vehiculos
"""

# ==========================================================
# IMPORTACIONES
# ==========================================================
from abc import ABC, abstractmethod

from utiles.utils import validar_matricula_esp


# ==========================================================
# CLASE ABSTRACTA VEHICULO
# ==========================================================
class Vehiculo(ABC):

    # ======================================================
    # REGISTROS GLOBALES
    # ======================================================

    matriculas_existentes = set()

    _vehiculos = []

    # ======================================================
    # CONSTRUCTOR
    # ======================================================

    def __init__(
            self,
            tipo,
            matricula,
            disponible=True,
            delegacion=None
    ):

        self._tipo = tipo.lower()

        self._matricula = matricula.upper()

        self._disponible = disponible

        self._delegacion = None

        # --------------------------------------------------
        # VALIDAR UNICIDAD
        # --------------------------------------------------
        if self._matricula in Vehiculo.matriculas_existentes:

            raise ValueError(
                f"La matrícula '{self._matricula}' ya existe"
            )

        Vehiculo.matriculas_existentes.add(
            self._matricula
        )

        Vehiculo._vehiculos.append(self)

        # --------------------------------------------------
        # ASIGNAR DELEGACIÓN
        # --------------------------------------------------
        if delegacion:
            self.asignar_delegacion(delegacion)

    # ======================================================
    # PROPIEDADES
    # ======================================================

    @property
    def tipo(self):
        return self._tipo

    @property
    def matricula(self):
        return self._matricula

    @property
    def disponible(self):
        return self._disponible

    @property
    def delegacion(self):
        return self._delegacion

    # ======================================================
    # DISPONIBILIDAD
    # ======================================================

    def ocupar(self):
        self._disponible = False

    def liberar(self):
        self._disponible = True

    # ======================================================
    # GESTIÓN DE DELEGACIÓN
    # ======================================================

    def asignar_delegacion(self, delegacion):

        if not delegacion.validar_vehiculo(self):

            raise ValueError(
                f"La delegación '{delegacion.nombre}' "
                f"no admite vehículos tipo '{self.tipo}'"
            )

        self._delegacion = delegacion

    def quitar_delegacion(self):

        self._delegacion = None

    # ======================================================
    # MÉTODOS DE CLASE
    # ======================================================

    @classmethod
    def vehiculos_registrados(cls):

        return cls._vehiculos

    # ======================================================
    # MÉTODOS ABSTRACTOS
    # ======================================================

    @abstractmethod
    def validar_matricula(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================

    def __str__(self):

        estado = (
            "Disponible"
            if self._disponible
            else "No disponible"
        )

        delegacion = (
            self._delegacion.nombre
            if self._delegacion
            else "Sin delegación"
        )

        return (
            f"{self._tipo} "
            f"{self._matricula} "
            f"({estado}) "
            f"| Delegación: {delegacion}"
        )


# ==========================================================
# CAMIÓN
# ==========================================================
class VehiculoCamion(Vehiculo):

    def __init__(
            self,
            matricula,
            disponible=True,
            delegacion=None
    ):

        super().__init__(
            "camion",
            matricula,
            disponible,
            delegacion
        )

    def validar_matricula(self):

        return validar_matricula_esp(
            self._matricula
        )

    def descripcion(self):

        return "Vehiculo de gran capacidad"


# ==========================================================
# FURGONETA
# ==========================================================
class VehiculoFurgoneta(Vehiculo):

    def __init__(
            self,
            matricula,
            disponible=True,
            delegacion=None
    ):

        super().__init__(
            "furgoneta",
            matricula,
            disponible,
            delegacion
        )

    def validar_matricula(self):

        return validar_matricula_esp(
            self._matricula
        )

    def descripcion(self):

        return "Vehiculo de reparto medio"


# ==========================================================
# MOTOCICLETA
# ==========================================================
class VehiculoMotocicleta(Vehiculo):

    def __init__(
            self,
            matricula,
            disponible=True,
            delegacion=None
    ):

        super().__init__(
            "motocicleta",
            matricula,
            disponible,
            delegacion
        )

    def validar_matricula(self):

        return validar_matricula_esp(
            self._matricula
        )

    def descripcion(self):

        return "Vehiculo rapido urbano"


# ==========================================================
# MOCHILA
# ==========================================================
class VehiculoMochila(Vehiculo):

    def __init__(
            self,
            matricula,
            disponible=True,
            delegacion=None
    ):

        super().__init__(
            "mochila",
            matricula,
            disponible,
            delegacion
        )

    def validar_matricula(self):

        if "-" not in self._matricula:
            return False

        partes = self._matricula.split("-")

        if len(partes) != 2:
            return False

        nombre, numero = partes

        if not nombre.isalpha():
            return False

        if not numero.isdigit():
            return False

        return True

    def descripcion(self):

        return "Reparto ligero"