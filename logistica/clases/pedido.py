"""
==========================================================
MÓDULO: pedido.py
==========================================================

Este módulo define la gestión completa de pedidos dentro del
sistema logístico.

Incluye:
✔ Clase Pedido (unidad básica de transporte)
✔ Clases GrupoPedidos (agrupación por fases logísticas)
✔ Subclases para cada fase:
    - Recogida
    - Transporte
    - Reparto
✔ Función de finalización de pedidos

RESPONSABILIDADES:
✔ Crear pedidos con datos logísticos
✔ Calcular distancia real entre clientes
✔ Gestionar estados del pedido
✔ Agrupar pedidos por fase operativa
✔ Controlar ciclo de vida del pedido

FLUJO DEL PEDIDO:
generado → en_recogida → en_transporte → en_reparto → entregado

NOTAS:
- La distancia se calcula automáticamente al crear el pedido
- El estado se actualiza dinámicamente según el grupo
- Los grupos permiten organizar rutas y operaciones
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utiles.utils import distancia_km


# ==========================================================
# CLASE PEDIDO (UNIDAD BÁSICA)
# ==========================================================
class Pedido:
    """
    Representa un pedido individual dentro del sistema logístico.
    """

    _contador = 0

    def __init__(self, origen, destino, peso, volumen,
                 fecha_entrega=None, nivel_servicio="standard"):
        """
        Inicializa un pedido.

        - origen / destino: objetos Cliente
        - peso: kg
        - volumen: litros
        - nivel_servicio: standard / express
        """

        # ==================================================
        # ID AUTOINCREMENTAL
        # ==================================================
        Pedido._contador += 1
        self._id = Pedido._contador

        # ==================================================
        # CLIENTES
        # ==================================================
        self._origen = origen
        self._destino = destino

        # ==================================================
        # DATOS LOGÍSTICOS
        # ==================================================
        self._peso = peso
        self._volumen = volumen
        self._nivel_servicio = nivel_servicio

        # ==================================================
        # FECHAS
        # ==================================================
        self._fecha_pedido = datetime.now()
        self._fecha_entrega = fecha_entrega

        # ==================================================
        # ESTADO DEL PEDIDO
        # ==================================================
        self._estado = "generado"

        # ==================================================
        # DISTANCIA REAL
        # ==================================================
        self._km = self.calcular_distancia()

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def id(self):
        """ID único del pedido"""
        return self._id

    @property
    def origen(self):
        """Cliente origen"""
        return self._origen

    @property
    def destino(self):
        """Cliente destino"""
        return self._destino

    @property
    def peso(self):
        return self._peso

    @property
    def volumen(self):
        return self._volumen

    @property
    def km(self):
        return self._km

    @property
    def estado(self):
        return self._estado

    @property
    def fecha_pedido(self):
        return self._fecha_pedido

    # ======================================================
    # CÁLCULO DE DISTANCIA
    # ======================================================
    def calcular_distancia(self):
        """
        Calcula la distancia geográfica entre origen y destino.

        ✔ Usa coordenadas de los clientes
        ✔ Devuelve km redondeados
        ✔ Si faltan datos → devuelve 0
        """

        if not self._origen.coordenadas or not self._destino.coordenadas:
            return 0

        return round(distancia_km(
            self._origen.coordenadas,
            self._destino.coordenadas
        ), 2)

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================
    def __str__(self):
        return (
            f"{self._id} | "
            f"{self._origen.nombre} → {self._destino.nombre} | "
            f"{self._km} km"
        )


# ==========================================================
# CLASE BASE: GRUPO DE PEDIDOS
# ==========================================================
class GrupoPedidos(ABC):
    """
    Clase abstracta que representa un conjunto de pedidos.

    Permite agrupar pedidos por fases logísticas.
    """

    _contador = 0

    def __init__(self):

        # ==================================================
        # ID DEL GRUPO
        # ==================================================
        GrupoPedidos._contador += 1
        self._id = GrupoPedidos._contador

        # ==================================================
        # LISTA DE PEDIDOS
        # ==================================================
        self._pedidos = []

        # ==================================================
        # FECHA DE CREACIÓN
        # ==================================================
        self._fecha_creacion = datetime.now()

        # ==================================================
        # ESTADO DEL GRUPO
        # ==================================================
        self._estado = "generado"

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def id(self):
        return self._id

    @property
    def pedidos(self):
        return self._pedidos

    @property
    def estado(self):
        return self._estado

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # ======================================================
    # MÉTODO BASE
    # ======================================================
    def agregar_pedido(self, pedido):
        """
        Añade un pedido al grupo.

        Este método puede ser sobrescrito en subclases
        para modificar el comportamiento (ej. cambiar estado).
        """
        self._pedidos.append(pedido)

    # ======================================================
    # REPRESENTACIÓN
    # ======================================================
    def __str__(self):
        return (
            f"Grupo {self._id} | "
            f"Pedidos: {len(self._pedidos)} | "
            f"Estado: {self._estado}"
        )


# ==========================================================
# GRUPO DE RECOGIDA
# ==========================================================
class GrupoPedidosRecogida(GrupoPedidos):
    """
    Grupo encargado de la recogida de pedidos.
    """

    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosRecogida._contador += 1
        self._id_recogida = GrupoPedidosRecogida._contador

    def agregar_pedido(self, pedido):
        """
        Cambia estado del pedido a 'en_recogida'
        y lo añade al grupo.
        """
        pedido._estado = "en_recogida"
        self._pedidos.append(pedido)


# ==========================================================
# GRUPO DE TRANSPORTE
# ==========================================================
class GrupoPedidosTransporte(GrupoPedidos):
    """
    Grupo encargado del transporte entre delegaciones.
    """

    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosTransporte._contador += 1
        self._id_transporte = GrupoPedidosTransporte._contador

    def agregar_pedido(self, pedido):
        pedido._estado = "en_transporte"
        self._pedidos.append(pedido)


# ==========================================================
# GRUPO DE REPARTO
# ==========================================================
class GrupoPedidosReparto(GrupoPedidos):
    """
    Grupo encargado de la entrega final al cliente.
    """

    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosReparto._contador += 1
        self._id_reparto = GrupoPedidosReparto._contador

    def agregar_pedido(self, pedido):
        pedido._estado = "en_reparto"
        self._pedidos.append(pedido)


# ==========================================================
# FINALIZACIÓN DEL PEDIDO
# ==========================================================
def finalizar_pedido(pedido):
    """
    Marca un pedido como entregado.

    ✔ Cambia estado → 'entregado'
    ✔ Asigna fecha de entrega actual
    """

    pedido._estado = "entregado"
    pedido._fecha_entrega = datetime.now()