# ==========================================================
# CLASE PEDIDO (UNIDAD)
# ==========================================================
from abc import ABC
from datetime import datetime

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utiles.utils import distancia_km


class Pedido:

    _contador = 0

    def __init__(self, origen, destino, peso, volumen, fecha_entrega=None, nivel_servicio="standard"):

        # ==========================
        # ID AUTOINCREMENTAL
        # ==========================
        Pedido._contador += 1
        self._id = Pedido._contador

        # ==========================
        # CLIENTES
        # ==========================
        self._origen = origen
        self._destino = destino

        # ==========================
        # DATOS LOGÍSTICOS
        # ==========================
        self._peso = peso
        self._volumen = volumen
        self._nivel_servicio = nivel_servicio

        # ==========================
        # FECHAS
        # ==========================
        self._fecha_pedido = datetime.now()   # 🔥 AUTOMÁTICO
        self._fecha_entrega = fecha_entrega

        # ==========================
        # ESTADO
        # ==========================
        self._estado_pedido = "generado"

        # ==========================
        # DISTANCIA REAL
        # ==========================
        self._km = self.calcular_distancia()


    # ==========================================
    # PROPIEDADES
    # ==========================================
    @property
    def id(self):
        return self._id

    @property
    def km(self):
        return self._km

    @property
    def estado_pedido(self):
        return self._estado_pedido

    @property
    def fecha_pedido(self):
        return self._fecha_pedido

    # ==========================================
    # DISTANCIA
    # ==========================================
    def calcular_distancia(self):

        if not self._origen.coordenadas or not self._destino.coordenadas:
            return 0

        from utiles.utils import distancia_km

        return round(distancia_km(
            self._origen.coordenadas,
            self._destino.coordenadas
        ), 2)

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def id(self):
        return self._id

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
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

    # ======================================================
    def __str__(self):
        return f"{self._id} | {self._origen.nombre} → {self._destino.nombre} | {self._km} km"

    # ==========================================================
    # GRUPOS DE PEDIDOS (CLASE BASE ABSTRACTA)
    # ==========================================================


class GrupoPedidos(ABC):
    _contador = 0

    def __init__(self):
        # ==========================
        # ID PROPIO DEL GRUPO
        # ==========================
        GrupoPedidos._contador += 1
        self._id = GrupoPedidos._contador

        # ==========================
        # LISTA DE PEDIDOS
        # ==========================
        self._pedidos = []

        # ==========================
        # FECHA CREACIÓN
        # ==========================
        self._fecha_creacion = datetime.now()

        # ==========================
        # ESTADO DEL GRUPO
        # ==========================
        self._estado_pedidos = "generado"

    # ==========================================
    # PROPIEDADES
    # ==========================================
    @property
    def id(self):
        return self._id

    @property
    def pedidos(self):
        return self._pedidos

    @property
    def estado(self):
        return self._estado_pedidos

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    # ==========================================
    # MÉTODO BASE (sobrescribible)
    # ==========================================
    def agregar_pedido(self, pedido):
        """
        Método genérico: añadir pedido al grupo
        (se puede especializar en subclases)
        """
        self._pedidos.append(pedido)

    # ==========================================
    # REPRESENTACIÓN
    # ==========================================
    def __str__(self):
        return (
            f"Grupo {self._id} | "
            f"Pedidos: {len(self._pedidos)} | "
            f"Estado: {self._estado_pedidos}"
        )

# ==========================================================
# GRUPO RECOGIDA
# ==========================================================
class GrupoPedidosRecogida(GrupoPedidos):
    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosRecogida._contador += 1
        self._id_recogida = GrupoPedidosRecogida._contador

    def agregar_pedido(self, pedido):
        """
        Añade pedido y actualiza estado individual
        """
        pedido._estado_pedido = "en_recogida"
        self._pedidos.append(pedido)

# ==========================================================
# GRUPO TRANSPORTE
# ==========================================================
class GrupoPedidosTransporte(GrupoPedidos):
    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosTransporte._contador += 1
        self._id_transporte = GrupoPedidosTransporte._contador

    def agregar_pedido(self, pedido):
        pedido._estado_pedido = "en_transporte"
        self._pedidos.append(pedido)

# ==========================================================
# GRUPO REPARTO
# ==========================================================
class GrupoPedidosReparto(GrupoPedidos):
    _contador = 0

    def __init__(self):
        super().__init__()

        GrupoPedidosReparto._contador += 1
        self._id_reparto = GrupoPedidosReparto._contador

    def agregar_pedido(self, pedido):
        pedido._estado_pedido = "en_reparto"
        self._pedidos.append(pedido)

# ==========================================================
# MÉTODO FINALIZAR PEDIDO (MUY IMPORTANTE)
# ==========================================================
def finalizar_pedido(pedido):
    """
    Marca un pedido como entregado y fija fecha de entrega
    """

    from datetime import datetime

    pedido._estado_pedido = "entregado"
    pedido._fecha_entrega = datetime.now()