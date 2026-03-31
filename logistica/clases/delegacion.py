"""
CLASES DELEGACIÓN DEL SISTEMA LOGÍSTICO

Este módulo define la jerarquía de clases que representan las delegaciones
del sistema logístico.

DESCRIPCIÓN GENERAL
------------------
Una delegación es un punto logístico desde el cual se gestionan vehículos
y operaciones de transporte.

El diseño sigue un modelo orientado a objetos con:

- Clase abstracta base: Delegacion
- Subclases:
    - DelegacionCentral
    - DelegacionDespacho

RESPONSABILIDADES
----------------
Cada delegación se encarga de:

- almacenar información básica (nombre, dirección, coordenadas)
- validar sus datos
- gestionar su flota de vehículos
- definir qué tipos de vehículos puede aceptar

CONCEPTOS UTILIZADOS
--------------------
- Herencia (Delegacion → Central / Despacho)
- Clase abstracta (ABC)
- Encapsulación (atributos privados con propiedades)
- Composición (Delegacion → Flota)
- Polimorfismo (validar_vehiculo)
- Uso de APIs externas (geocoding con geopy)

OBJETIVO
--------
Modelar el comportamiento real de distintos tipos de delegaciones
en un sistema logístico.
"""


# ==========================================================
# IMPORTACIONES
# ==========================================================

from abc import ABC, abstractmethod   # Para crear clases abstractas
from geopy.geocoders import Nominatim  # Para convertir dirección en coordenadas
from clases.flota import Flota        # Relación de composición (Delegacion → Flota)

# Importamos tipos de vehículos para validaciones
from clases.vehiculo import (
    VehiculoCamion,
    VehiculoFurgoneta,
    VehiculoMotocicleta,
    VehiculoMochila
)


# ==========================================================
# CLASE ABSTRACTA DELEGACION
# ==========================================================

class Delegacion(ABC):
    """
    Clase base abstracta para todas las delegaciones.

    No se puede instanciar directamente.
    Define la estructura y comportamiento común.
    """

    # Conjunto para evitar nombres duplicados
    nombres_existentes = set()

    def __init__(self, nombre, direccion):

        # Atributos privados (encapsulación)
        self._nombre = nombre
        self._direccion = direccion
        self._coordenadas = None
        self._flota = None

    # ------------------------------------------------------
    # PROPIEDADES (GETTERS)
    # ------------------------------------------------------

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
    def flota(self):
        return self._flota

    # ------------------------------------------------------
    # MÉTODO: ASIGNAR FLOTA
    # ------------------------------------------------------

    def asignar_flota(self):
        """
        Crea una flota asociada a la delegación.

        Relación de composición:
        Una delegación contiene una flota.
        """
        self._flota = Flota(self)

    # ------------------------------------------------------
    # VALIDACIÓN DE NOMBRE
    # ------------------------------------------------------

    def validar_nombre(self):
        """
        Comprueba que el nombre de la delegación no esté repetido.

        Utiliza un conjunto (set) para almacenar nombres existentes.
        """

        if self._nombre in Delegacion.nombres_existentes:
            return False

        Delegacion.nombres_existentes.add(self._nombre)
        return True

    # ------------------------------------------------------
    # VALIDACIÓN DE DIRECCIÓN
    # ------------------------------------------------------

    def validar_direccion(self):
        """
        Valida la dirección usando geocoding.

        Convierte la dirección en coordenadas geográficas
        mediante la API de OpenStreetMap (Nominatim).
        """

        geolocator = Nominatim(user_agent="logistica_app")

        try:
            location = geolocator.geocode(self._direccion)

            if location:
                # Guardamos coordenadas (latitud, longitud)
                self._coordenadas = (location.latitude, location.longitude)
                return True

            return False

        except:
            # Manejo de errores (fallos de conexión, etc.)
            return False

    # ------------------------------------------------------
    # MÉTODO ABSTRACTO
    # ------------------------------------------------------

    @abstractmethod
    def validar_vehiculo(self, vehiculo):
        """
        Método abstracto que debe implementar cada tipo de delegación.

        Define qué tipos de vehículos son válidos.
        """
        pass

    # ------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO
    # ------------------------------------------------------

    def __str__(self):
        """
        Devuelve una representación en texto de la delegación.
        """

        total = 0
        if self._flota:
            total = len(self._flota.vehiculos)

        return f"{self._nombre} | {self._direccion} | {self._coordenadas} | Vehiculos: {total}"


# ==========================================================
# DELEGACIÓN CENTRAL
# ==========================================================

class DelegacionCentral(Delegacion):
    """
    Delegación principal.

    Permite vehículos de mayor capacidad.
    """

    def validar_vehiculo(self, vehiculo):
        """
        Solo permite:
        - Camiones
        - Furgonetas
        - Motocicletas
        """

        return isinstance(
            vehiculo,
            (VehiculoCamion, VehiculoFurgoneta, VehiculoMotocicleta)
        )


# ==========================================================
# DELEGACIÓN DESPACHO
# ==========================================================

class DelegacionDespacho(Delegacion):
    """
    Delegación secundaria (reparto local).

    No permite vehículos pesados.
    """

    def validar_vehiculo(self, vehiculo):
        """
        Solo permite:
        - Furgonetas
        - Motocicletas
        - Mochilas
        """

        return isinstance(
            vehiculo,
            (VehiculoFurgoneta, VehiculoMotocicleta, VehiculoMochila)
        )