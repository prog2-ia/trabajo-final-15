"""
CLASES VEHÍCULO DEL SISTEMA LOGÍSTICO

Este módulo define la jerarquía de vehículos utilizados en el sistema logístico.

DESCRIPCIÓN GENERAL
------------------
La clase Vehiculo es una clase abstracta que representa un medio de transporte.
A partir de ella se definen distintos tipos de vehículos:

- Camión
- Furgoneta
- Motocicleta
- Mochila

Cada tipo de vehículo tiene sus propias reglas de validación.

RESPONSABILIDADES
----------------
Cada vehículo se encarga de:

- almacenar su información básica (tipo, matrícula, estado)
- validar su matrícula
- controlar su disponibilidad
- proporcionar una descripción del tipo de vehículo

CONCEPTOS UTILIZADOS
--------------------
- Clase abstracta (ABC)
- Herencia (Vehiculo → subclases)
- Encapsulación (atributos privados + propiedades)
- Polimorfismo (validar_matricula, descripcion)
- Validación de datos
- Uso de conjuntos para unicidad

OBJETIVO
--------
Modelar distintos tipos de transporte dentro del sistema logístico,
aplicando restricciones y validaciones propias de cada uno.
"""


# ==========================================================
# IMPORTACIONES
# ==========================================================

from abc import ABC, abstractmethod   # Para definir clase abstracta
from utiles.utils import validar_matricula_esp  # Validación de matrículas españolas


# ==========================================================
# CLASE ABSTRACTA VEHICULO
# ==========================================================

class Vehiculo(ABC):
    """
    Clase base abstracta para todos los vehículos.

    No se puede instanciar directamente.
    Define atributos y comportamientos comunes.
    """

    # Conjunto para controlar que no haya matrículas duplicadas
    matriculas_existentes = set()

    def __init__(self, tipo, matricula, disponible=True):

        # Atributos privados (encapsulación)
        self._tipo = tipo.lower()
        self._matricula = matricula.upper()
        self._disponible = disponible

    # ------------------------------------------------------
    # PROPIEDADES (GETTERS)
    # ------------------------------------------------------

    @property
    def tipo(self):
        return self._tipo

    @property
    def matricula(self):
        return self._matricula

    @property
    def disponible(self):
        return self._disponible

    # ------------------------------------------------------
    # GESTIÓN DE DISPONIBILIDAD
    # ------------------------------------------------------

    def ocupar(self):
        """
        Marca el vehículo como no disponible.
        """
        self._disponible = False

    def liberar(self):
        """
        Marca el vehículo como disponible.
        """
        self._disponible = True

    # ------------------------------------------------------
    # VALIDACIÓN DE UNICIDAD
    # ------------------------------------------------------

    def validar_unicidad(self):
        """
        Comprueba que la matrícula no esté repetida en el sistema.

        Usa un conjunto (set) para asegurar unicidad.
        """

        if self._matricula in Vehiculo.matriculas_existentes:
            return False

        Vehiculo.matriculas_existentes.add(self._matricula)
        return True

    # ------------------------------------------------------
    # MÉTODOS ABSTRACTOS
    # ------------------------------------------------------

    @abstractmethod
    def validar_matricula(self):
        """
        Método abstracto que valida la matrícula según el tipo de vehículo.
        """
        pass

    @abstractmethod
    def descripcion(self):
        """
        Devuelve una descripción del vehículo.
        """
        pass

    # ------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO
    # ------------------------------------------------------

    def __str__(self):
        """
        Devuelve una representación en texto del vehículo.
        """

        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self._tipo} {self._matricula} ({estado})"


# ==========================================================
# CAMION
# ==========================================================

class VehiculoCamion(Vehiculo):
    """
    Vehículo de gran capacidad para transporte pesado.
    """

    def __init__(self, matricula, disponible=True):
        super().__init__("camion", matricula, disponible)

    def validar_matricula(self):
        """
        Valida matrícula española estándar.
        """

        if not validar_matricula_esp(self._matricula):
            return False

        return self.validar_unicidad()

    def descripcion(self):
        return "Vehiculo de gran capacidad"


# ==========================================================
# FURGONETA
# ==========================================================

class VehiculoFurgoneta(Vehiculo):
    """
    Vehículo de reparto medio.
    """

    def __init__(self, matricula, disponible=True):
        super().__init__("furgoneta", matricula, disponible)

    def validar_matricula(self):

        if not validar_matricula_esp(self._matricula):
            return False

        return self.validar_unicidad()

    def descripcion(self):
        return "Vehiculo de reparto medio"


# ==========================================================
# MOTOCICLETA
# ==========================================================

class VehiculoMotocicleta(Vehiculo):
    """
    Vehículo rápido para transporte urbano.
    """

    def __init__(self, matricula, disponible=True):
        super().__init__("motocicleta", matricula, disponible)

    def validar_matricula(self):

        if not validar_matricula_esp(self._matricula):
            return False

        return self.validar_unicidad()

    def descripcion(self):
        return "Vehiculo rapido urbano"


# ==========================================================
# MOCHILA
# ==========================================================

class VehiculoMochila(Vehiculo):
    """
    Representa un repartidor a pie o bicicleta.

    Utiliza un formato de identificación distinto a una matrícula tradicional.
    """

    def __init__(self, matricula, disponible=True):
        super().__init__("mochila", matricula, disponible)

    def validar_matricula(self):
        """
        Valida formato especial: Nombre-Numero
        Ejemplo: Alicante-1
        """

        if not self._matricula:
            return False

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

        return self.validar_unicidad()

    def descripcion(self):
        return "Reparto ligero"