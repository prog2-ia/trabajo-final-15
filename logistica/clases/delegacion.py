from abc import ABC

from clases.flota import Flota
from utiles.geolocalizacion import geocodificar


class Delegacion(ABC):
    nombres_existentes = set()

    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):

        if nombre in Delegacion.nombres_existentes:
            raise ValueError(f"Nombre duplicado: {nombre}")

        Delegacion.nombres_existentes.add(nombre)

        self._nombre = nombre
        self._direccion = direccion
        self._delegacion_superior = delegacion_superior
        self.provincia = provincia

        self._coordenadas = None
        self._flota = None

    # ======================================================
    # COORDENADAS
    # ======================================================
    def calcular_coordenadas(self):

        if self._coordenadas:
            return

        self._coordenadas = geocodificar(self.direccion)

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def coordenadas(self):
        return self._coordenadas

    @property
    def nombre(self):
        return self._nombre

    @property
    def direccion(self):
        return self._direccion

    @property
    def provincia(self):
        return self._provincia

    @provincia.setter
    def provincia(self, valor):
        self._provincia = valor.lower() if valor else None

    @property
    def flota(self):
        return self._flota

    @property
    def delegacion_superior(self):
        return self._delegacion_superior

    # ======================================================
    # MÉTODOS
    # ======================================================
    def asignar_flota(self):
        self._flota = Flota(self)

    def validar_direccion(self):
        coords = geocodificar(self._direccion)

        if coords:
            self._coordenadas = coords
            return True
        return False

    def __str__(self):
        sup = self._delegacion_superior.nombre if self._delegacion_superior else "Ninguna"
        total = len(self._flota.vehiculos) if self._flota else 0
        return f"{self._nombre} | Sup:{sup} | Vehiculos:{total}"


# ==========================================================
# SUBCLASES
# ==========================================================
from clases.vehiculo import VehiculoCamion, VehiculoFurgoneta


class DelegacionCentral(Delegacion):
    def __init__(self, nombre, direccion, provincia=None):
        super().__init__(nombre, direccion, None, provincia)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoCamion)


class DelegacionBase(Delegacion):
    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):
        super().__init__(nombre, direccion, delegacion_superior, provincia)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoFurgoneta)


class DelegacionDespacho(Delegacion):
    def __init__(self, nombre, direccion, delegacion_superior=None, provincia=None):
        super().__init__(nombre, direccion, delegacion_superior, provincia)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoFurgoneta)
