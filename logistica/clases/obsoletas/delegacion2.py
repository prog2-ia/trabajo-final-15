"""
==========================================================
MÓDULO: delegacion2.py
==========================================================

Este módulo define la jerarquía de delegaciones dentro del sistema logístico.

Responsabilidades principales:
✔ Representar una delegación (central, base o despacho)
✔ Gestionar su dirección y coordenadas geográficas
✔ Asociar una flota de vehículos
✔ Controlar la relación jerárquica entre delegaciones
✔ Validar los tipos de vehículos permitidos según el tipo de delegación

Estructura:
- Clase abstracta Delegacion (base común)
- Subclases:
    - DelegacionCentral → solo camiones de gran tonelaje
    - DelegacionBase → furgonetas o camiones de mediano tonelaje
    - DelegacionDespacho → furgonetas de reparto o motocicletas o mochilas

Notas importantes:
- Se evita duplicidad de nombres mediante un registro global
- La geolocalización se realiza bajo demanda
- La flota se asigna dinámicamente
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC

from clases.flota import Flota
from utiles.geolocalizacion import geocodificar


# ==========================================================
# CLASE BASE: DELEGACION
# ==========================================================
class Delegacion(ABC):
    """
    Clase abstracta que define el comportamiento común de todas las delegaciones.
    """

    # ------------------------------------------------------
    # CONTROL DE NOMBRES ÚNICOS
    # ------------------------------------------------------
    # nombres_existentes = set()
    nombres_existentes: set[str] = set()

    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):
        """
        Inicializa una delegación.

        - nombre: identificador único
        - direccion: dirección física
        - delegacion_superior: jerarquía (opcional)
        - provincia: ubicación geográfica
        """

        # Validación de nombres únicos
        if nombre in Delegacion.nombres_existentes:
            raise ValueError(f"Nombre duplicado: {nombre}")

        Delegacion.nombres_existentes.add(nombre)

        # Asignación de atributos principales
        self._nombre = nombre
        self._direccion = direccion
        self._delegacion_superior = delegacion_superior
        self.provincia = provincia

        # Inicialización diferida
        self._coordenadas = None
        self._flota = None

    # ======================================================
    # COORDENADAS
    # ======================================================
    def calcular_coordenadas(self):
        """
        Calcula las coordenadas geográficas de la delegación.

        ✔ Usa geocodificación de la dirección
        ✔ Solo se ejecuta si no están ya calculadas (lazy loading)
        """

        if self._coordenadas:
            return

        self._coordenadas = geocodificar(self.direccion)

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def coordenadas(self):
        """Devuelve las coordenadas geográficas"""
        return self._coordenadas

    @property
    def nombre(self):
        """Devuelve el nombre de la delegación"""
        return self._nombre

    @property
    def direccion(self):
        """Devuelve la dirección"""
        return self._direccion

    @property
    def provincia(self):
        """Devuelve la provincia"""
        return self._provincia

    @provincia.setter
    def provincia(self, valor):
        """
        Normaliza la provincia:
        ✔ Se guarda en minúsculas
        ✔ Permite None
        """
        self._provincia = valor.lower() if valor else None

    @property
    def flota(self):
        """Devuelve la flota asociada"""
        return self._flota

    @property
    def delegacion_superior(self):
        """Devuelve la delegación jerárquica superior"""
        return self._delegacion_superior

    # ======================================================
    # MÉTODOS
    # ======================================================
    def asignar_flota(self):
        """
        Asigna una flota a la delegación.

        ✔ Crea una instancia de Flota
        ✔ Establece relación bidireccional

         Por desarrollar
        """
        self._flota = Flota(self)

    def validar_direccion(self):
        """
        Verifica que la dirección es válida mediante geocodificación.

        ✔ Si es válida → guarda coordenadas
        ✔ Si no → devuelve False
        """
        coords = geocodificar(self._direccion)

        if coords:
            self._coordenadas = coords
            return True

        return False

    def __str__(self):
        """
        Representación en texto de la delegación.

        Incluye:
        - Nombre
        - Delegación superior
        - Número de vehículos
        """
        sup = self._delegacion_superior.nombre if self._delegacion_superior else "Ninguna"
        total = len(self._flota.vehiculos) if self._flota else 0

        return f"{self._nombre} | Sup:{sup} | Vehiculos:{total}"


# ==========================================================
# SUBCLASES DE DELEGACION
# ==========================================================

from clases.vehiculo import VehiculoCamion, VehiculoFurgoneta


# ----------------------------------------------------------
# DELEGACION CENTRAL
# ----------------------------------------------------------
class DelegacionCentral(Delegacion):
    """
    Delegación principal del sistema.

    ✔ No tiene delegación superior
    ✔ Solo admite vehículos tipo camión de gran tonelaje
    """

    def __init__(self, nombre, direccion, provincia=None):
        super().__init__(nombre, direccion, None, provincia)

    def validar_vehiculo(self, vehiculo):
        """Solo permite camiones"""
        return isinstance(vehiculo, VehiculoCamion)


# ----------------------------------------------------------
# DELEGACION BASE
# ----------------------------------------------------------
class DelegacionBase(Delegacion):
    """
    Delegación intermedia.

    ✔ Puede depender de una central
    ✔ Gestiona distribución regional
    ✔ Solo admite furgonetas o camiones de mediano tonelaje
    """

    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):
        super().__init__(nombre, direccion, delegacion_superior, provincia)

    def validar_vehiculo(self, vehiculo):
        """Solo permite furgonetas"""
        return isinstance(vehiculo, VehiculoFurgoneta)


# ----------------------------------------------------------
# DELEGACION DESPACHO
# ----------------------------------------------------------
class DelegacionDespacho(Delegacion):
    """
    Delegación de última milla.

    ✔ Último punto antes del cliente
    ✔ Depende de una base o central
    ✔ Solo admite furgonetas o motocicletas o mochilas
    """

    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):
        super().__init__(nombre, direccion, delegacion_superior, provincia)

    def validar_vehiculo(self, vehiculo):
        """Solo permite furgonetas"""
        return isinstance(vehiculo, VehiculoFurgoneta)