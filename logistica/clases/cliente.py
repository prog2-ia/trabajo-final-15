"""
CLASE CLIENTE

Este módulo define la clase Cliente del sistema logístico.

FUNCIONALIDAD

Representa un cliente que puede:
- Ser origen o destino de pedidos
- Tener pedidos en curso y finalizados
- Acumular importe facturado

CAMBIOS IMPORTANTES
- La dirección ahora es un STRING (no objeto Direccion)
- Se añade coordenadas geográficas
- Se añade delegación cercana (objeto Delegacion)

Esto simplifica la persistencia y mejora el rendimiento del sistema
"""


class Cliente:

    def __init__(self, dni, nombre, apellidos, direccion, provincia=None, delegacion_cercana=None):

        # ==========================
        # DATOS BASICOS
        # ==========================
        self._dni = dni
        self._nombre = nombre
        self._apellidos = apellidos

        # direccion ahora es STRING
        self._direccion = direccion
        self._provincia = provincia

        # nueva arquitectura
        self._coordenadas = None
        self._delegacion_cercana = delegacion_cercana
        self._distancia_despacho = None

        # ==========================
        # PEDIDOS
        # ==========================
        self._pedidos_en_curso = []
        self._pedidos_terminados = []

        self._importe_facturado = 0

    # ==========================================
    # GETTERS
    # ==========================================

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
    def provincia(self):
        return self._provincia

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

    # ==========================================
    # OPERADORES
    # ==========================================

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

    # ==========================================
    # REPRESENTACION
    # ==========================================

    def __str__(self):

        return (
            f"DNI: {self._dni}\n"
            f"{self._apellidos}, {self._nombre}\n"
            f"Direccion: {self._direccion}\n"
            f"Provincia: {self._provincia}\n"
            f"Coordenadas: {self._coordenadas}\n"
            f"Delegacion: {self._delegacion_cercana.nombre if self._delegacion_cercana else 'N/A'}\n"
            f"Importe: {round(self._importe_facturado, 2)}\n"
            f"Distancia al despacho: {self._distancia_despacho} km\n"
        )
