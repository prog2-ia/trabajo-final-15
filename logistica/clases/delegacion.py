from abc import ABC
from clases.flota import Flota
from utiles.utils import (geocodificar_direccion, geocodificar_con_cache)



class Delegacion(ABC):

    nombres_existentes = set()

    def __init__(self, nombre, direccion, provincia=None, delegacion_superior=None):

        if nombre in Delegacion.nombres_existentes:
            raise ValueError(f"Nombre duplicado: {nombre}")

        Delegacion.nombres_existentes.add(nombre)

        self._nombre = nombre
        self._direccion = direccion
        self.provincia = provincia
        self._delegacion_superior = delegacion_superior

        #  NO geocodificar aquí
        self._coordenadas = None

        self._flota = None

    # ======================================================
    # MÉTODO NUEVO
    # ======================================================

    def calcular_coordenadas(self):
        """
        Calcula coordenadas usando cache para evitar llamadas repetidas
        """

        if hasattr(self, "_coordenadas") and self._coordenadas:
            return  # ya calculadas

        self._coordenadas = geocodificar_con_cache(self.direccion)



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
        coords = geocodificar_direccion(self._direccion)
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
    def __init__(self, nombre, direccion,provincia=None, delegacion_superior=None):
        super().__init__(nombre, direccion, None)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoCamion)


class DelegacionBase(Delegacion):
    def __init__(self, nombre, direccion, provincia=None, delegacion_superior=None):
        super().__init__(nombre, direccion, provincia, delegacion_superior)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoFurgoneta)


class DelegacionDespacho(Delegacion):
    def __init__(self, nombre, direccion, provincia=None, delegacion_superior=None):
        super().__init__(nombre, direccion, provincia, delegacion_superior)

    def validar_vehiculo(self, vehiculo):
        return isinstance(vehiculo, VehiculoFurgoneta)