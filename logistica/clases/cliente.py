"""
CLASE CLIENTE (VERSIÓN PRO FINAL)

✔ Dirección = STRING
✔ Coordenadas geográficas
✔ Población real (reverse geocoding)
✔ Provincia real (reverse geocoding)
✔ Delegación cercana
✔ Distancia al despacho

OPTIMIZACIÓN:
✔ Reverse geocoding unificado (1 sola llamada)
✔ Cache interno en geolocalización
"""
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utiles.geolocalizacion import obtener_datos_geo


class Cliente:

    def __init__(self, dni, nombre, apellidos, direccion,
                 provincia=None, delegacion_cercana=None):

        # ==========================
        # DATOS BASICOS
        # ==========================
        self._dni = dni
        self._nombre = nombre
        self._apellidos = apellidos
        self._direccion = direccion

        # ==========================
        # DATOS GEO
        # ==========================
        self._coordenadas = None
        self._poblacion = None
        self._provincia = None




        # ==========================
        # LOGÍSTICA
        # ==========================
        self._delegacion_cercana = delegacion_cercana
        self._distancia_despacho = None

        # ==========================
        # PEDIDOS
        # ==========================
        self._pedidos_en_curso = []
        self._pedidos_terminados = []
        self._importe_facturado = 0

    # ======================================================
    # MÉTODO CLAVE (NUEVO)
    # ======================================================
    def actualizar_datos_geo(self):
        """
        Actualiza población y provincia a partir de coordenadas.
        """

        if not self._coordenadas:
            return

        from utiles.geolocalizacion import obtener_datos_geo

        poblacion, provincia = obtener_datos_geo(self._coordenadas)

        self._poblacion = poblacion
        self._provincia = provincia
    # ======================================================
    # GETTERS
    # ======================================================
    @property
    def dni(self):
        return self._dni

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellidos(self):
        return self._apellidos

    @property
    def direccion(self):
        return self._direccion

    @property
    def poblacion(self):
        return self._poblacion or "N/A"

    @property
    def provincia(self):
        return self._provincia or "N/A"



    @property
    def coordenadas(self):
        return self._coordenadas

    @property
    def delegacion_cercana(self):
        return self._delegacion_cercana

    @delegacion_cercana.setter
    def delegacion_cercana(self, value):
        self._delegacion_cercana = value

    @property
    def distancia_despacho(self):
        return self._distancia_despacho

    # ======================================================
    # OPERADORES
    # ======================================================
    def __add__(self, pedido):
        self._pedidos_en_curso.append(pedido)
        return self

    def __sub__(self, pedido):
        if pedido in self._pedidos_en_curso:
            self._pedidos_en_curso.remove(pedido)
            self._pedidos_terminados.append(pedido)

            if hasattr(pedido, "km") and pedido.km:
                self._importe_facturado += pedido.km

        return self

    # ======================================================
    # REPRESENTACION
    # ======================================================
    def __str__(self):

        return (
            f"DNI: {self._dni}\n"
            f"{self._apellidos}, {self._nombre}\n"
            f"Direccion: {self._direccion}\n"
            f"Población: {self._poblacion}\n"
            f"Provincia: {self._provincia}\n"
            f"Coordenadas: {self._coordenadas}\n"
            f"Delegacion: {self._delegacion_cercana.nombre if self._delegacion_cercana else 'N/A'}\n"
            f"Distancia despacho: {self._distancia_despacho} km\n"
            f"Importe: {round(self._importe_facturado, 2)}\n"
        )