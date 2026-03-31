"""
CLASE FLOTA DEL SISTEMA LOGÍSTICO

Este módulo define la clase Flota, que representa el conjunto de vehículos
asociados a una delegación.

DESCRIPCIÓN GENERAL
------------------
La clase Flota actúa como un contenedor de vehículos, gestionando su almacenamiento
y operaciones básicas como añadir, eliminar y consultar vehículos.

Cada flota está asociada a una delegación, lo que implica que:

- La delegación define qué vehículos son válidos.
- La flota delega en la delegación la validación de los vehículos.

RESPONSABILIDADES
----------------
La clase Flota se encarga de:

- almacenar vehículos
- añadir vehículos (respetando restricciones)
- eliminar vehículos
- listar vehículos
- obtener vehículos disponibles

CONCEPTOS UTILIZADOS
--------------------
- Composición (Delegacion → Flota → Vehiculos)
- Encapsulación (atributos privados)
- Delegación de responsabilidad (validación en Delegacion)
- Listas y comprensión de listas

OBJETIVO
--------
Gestionar de forma centralizada los vehículos de una delegación.
"""


# ==========================================================
# CLASE FLOTA
# ==========================================================

class Flota:
    """
    Representa el conjunto de vehículos de una delegación.
    """

    def __init__(self, delegacion):
        """
        Constructor de la clase.

        Parámetros:
        - delegacion: objeto Delegacion al que pertenece la flota
        """

        # Relación de composición: la flota pertenece a una delegación
        self._delegacion = delegacion

        # Lista de vehículos
        self._vehiculos = []

    # ------------------------------------------------------
    # PROPIEDAD VEHICULOS
    # ------------------------------------------------------

    @property
    def vehiculos(self):
        """
        Devuelve la lista de vehículos de la flota.
        """
        return self._vehiculos

    # ------------------------------------------------------
    # AÑADIR VEHÍCULO
    # ------------------------------------------------------

    def añadir_vehiculo(self, vehiculo):
        """
        Añade un vehículo a la flota.

        Antes de añadirlo, se valida con la delegación si el vehículo es permitido.

        Parámetro:
        - vehiculo: objeto Vehiculo

        Devuelve:
        - True si se añade correctamente
        - False si no está permitido
        """

        # Validación delegada a la clase Delegacion
        if self._delegacion.validar_vehiculo(vehiculo):
            self._vehiculos.append(vehiculo)
            return True

        return False

    # ------------------------------------------------------
    # ELIMINAR VEHÍCULO
    # ------------------------------------------------------

    def quitar_vehiculo(self, vehiculo):
        """
        Elimina un vehículo de la flota.

        Parámetro:
        - vehiculo: objeto Vehiculo

        Devuelve:
        - True si se elimina correctamente
        - False si no existe en la flota
        """

        if vehiculo in self._vehiculos:
            self._vehiculos.remove(vehiculo)
            return True

        return False

    # ------------------------------------------------------
    # LISTAR VEHÍCULOS
    # ------------------------------------------------------

    def listar_vehiculos(self):
        """
        Devuelve una lista de strings con la representación de los vehículos.

        Utiliza comprensión de listas.
        """

        return [str(v) for v in self._vehiculos]

    # ------------------------------------------------------
    # VEHÍCULOS DISPONIBLES
    # ------------------------------------------------------

    def vehiculos_disponibles(self):
        """
        Devuelve una lista de vehículos que están disponibles.

        Filtra por el atributo 'disponible'.
        """

        return [v for v in self._vehiculos if v.disponible]

    # ------------------------------------------------------
    # REPRESENTACIÓN EN TEXTO
    # ------------------------------------------------------

    def __str__(self):
        """
        Devuelve una representación en texto de la flota.
        """

        return f"Vehiculos: {self.listar_vehiculos()}"