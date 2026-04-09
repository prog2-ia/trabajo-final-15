# ==========================================================
# SISTEMA DE PEDIDOS COMPLETO (CON AUTOMATISMO DE ESTADOS)
# ==========================================================
"""
ARQUITECTURA DEL SISTEMA

Este módulo implementa un sistema logístico realista basado en:

✔ Pedido (unidad individual)
✔ GrupoPedidos (contenedor abstracto)
✔ Grupos derivados:
    - GrupoRecogida
    - GrupoTransporte
    - GrupoReparto

----------------------------------------------------------
CARACTERÍSTICAS PRINCIPALES
----------------------------------------------------------

✔ Encapsulamiento completo
✔ IDs automáticos y únicos
✔ Fechas:
    - Pedido → fecha_pedido
    - Grupo → fecha_creacion
✔ Estados:
    - Pedido → estado individual
    - Grupo → estado global automático

----------------------------------------------------------
SISTEMA AUTOMÁTICO DE ESTADOS
----------------------------------------------------------

Este sistema implementa un comportamiento REACTIVO:

👉 Cuando cambia un pedido → el grupo se actualiza automáticamente
👉 No hay inconsistencias entre pedidos y grupo

Esto sigue un patrón tipo:
✔ Observer Pattern (simplificado)
✔ Sistema dirigido por eventos

----------------------------------------------------------
REGLAS DE ESTADO DEL GRUPO
----------------------------------------------------------

- Si todos los pedidos están FINALIZADOS → grupo FINALIZADO
- Si todos están ENTREGADOS → grupo ENTREGADO
- Si alguno está en transporte/reparto → grupo EN TRANSPORTE
- Si alguno está en recogida → grupo EN TRANSPORTE
- Si no → grupo GENERADO

----------------------------------------------------------
VENTAJAS
----------------------------------------------------------

✔ Cohesión total de datos
✔ Automatización completa
✔ Escalable (rutas, tracking, IA)
✔ Preparado para sistemas reales tipo SEUR / Amazon
"""

# ==========================================================
# IMPORTS
# ==========================================================
from abc import ABC
from datetime import datetime
from utiles.utils import distancia_km


# ==========================================================
# ESTADOS PERMITIDOS
# ==========================================================
ESTADOS_PEDIDO = {
    "generado",
    "en_recogida",
    "en_transporte",
    "en_reparto",
    "entregado",
    "finalizado"
}

ESTADOS_GRUPO = {
    "generado",
    "en_transporte",
    "entregado",
    "finalizado"
}


# ==========================================================
# CLASE PEDIDO
# ==========================================================
class Pedido:

    _contador = 0

    def __init__(
        self,
        origen,
        destino,
        peso,
        volumen,
        fecha_entrega,
        nivel_servicio,
        fecha_pedido=None,
        estado_pedido="generado"
    ):

        # ------------------------------
        # VALIDACIONES
        # ------------------------------
        if origen == destino:
            raise ValueError("Origen y destino no pueden ser iguales")

        if peso <= 0:
            raise ValueError("Peso inválido")

        if volumen <= 0:
            raise ValueError("Volumen inválido")

        if not origen.coordenadas or not destino.coordenadas:
            raise ValueError("Clientes sin coordenadas")

        if estado_pedido not in ESTADOS_PEDIDO:
            raise ValueError(f"Estado inválido: {estado_pedido}")

        # ------------------------------
        # ID GLOBAL SECUENCIAL
        # ------------------------------
        Pedido._contador += 1
        self._id = f"P{Pedido._contador}"

        # ------------------------------
        # DATOS DEL PEDIDO
        # ------------------------------
        self._origen = origen
        self._destino = destino
        self._peso = peso
        self._volumen = volumen
        self._fecha_entrega = None
        self._nivel_servicio = nivel_servicio

        self._fecha_pedido = fecha_pedido or datetime.now()
        self._estado_pedido = estado_pedido

        # ------------------------------
        # COORDENADAS REALES
        # ------------------------------
        self._coord_origen = origen.coordenadas
        self._coord_destino = destino.coordenadas

        # ------------------------------
        # DISTANCIA REAL (HAVERSINE)
        # ------------------------------
        self._km = round(
            distancia_km(self._coord_origen, self._coord_destino),
            2
        )

        # REFERENCIA AL GRUPO (para sistema automático)
        self._grupo = None

    # ======================================================
    # MÉTODO PARA ENLAZAR CON GRUPO
    # ======================================================
    def set_grupo(self, grupo):
        """
        Permite que el pedido conozca su grupo.

        Esto es clave para el sistema reactivo:
        → cuando cambia el pedido → notifica al grupo
        """
        self._grupo = grupo

    # ======================================================
    # CAMBIO DE ESTADO (REACTIVO)
    # ======================================================
    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del pedido.

        🔥 NUEVO COMPORTAMIENTO:
        - Si pasa a 'entregado' → se registra fecha_entrega
        - Sistema reactivo: notifica al grupo
        """

        if nuevo_estado not in ESTADOS_PEDIDO:
            raise ValueError(f"Estado inválido: {nuevo_estado}")

        self._estado_pedido = nuevo_estado

        # --------------------------------------------------
        # 📦 REGISTRAR FECHA DE ENTREGA
        # --------------------------------------------------
        if nuevo_estado == "entregado" and self._fecha_entrega is None:
            from datetime import datetime
            self._fecha_entrega = datetime.now()

        # --------------------------------------------------
        # 🔥 SISTEMA REACTIVO (grupo)
        # --------------------------------------------------
        if self._grupo:
            self._grupo.actualizar_estado()


    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def estado_pedido(self):
        return self._estado_pedido

    @property
    def id(self):
        return self._id

    @property
    def km(self):
        return self._km

    @property
    def origen(self):
        return self._origen

    @property
    def destino(self):
        return self._destino

    @property
    def fecha_entrega(self):
        return self._fecha_entrega

    # ======================================================
    def __str__(self):
        return (
            f"{self._id} | "
            f"{self._origen.nombre} → {self._destino.nombre} | "
            f"{self._estado_pedido} | "
            f"Entrega: {self._fecha_entrega if self._fecha_entrega else 'Pendiente'}"
        )


# ==========================================================
# CLASE BASE GRUPO PEDIDOS
# ==========================================================
class GrupoPedidos(ABC):

    def __init__(self, estado_pedidos="generado"):

        if estado_pedidos not in ESTADOS_GRUPO:
            raise ValueError(f"Estado inválido: {estado_pedidos}")

        self._fecha_creacion = datetime.now()
        self._pedidos = []
        self._estado_pedidos = estado_pedidos

    # ======================================================
    # SISTEMA AUTOMÁTICO DE ESTADO
    # ======================================================
    def actualizar_estado(self):
        """
        🔥 FUNCIÓN CLAVE DEL SISTEMA

        Analiza los estados de todos los pedidos
        y determina el estado global del grupo.

        ✔ Sistema automático
        ✔ Sin intervención manual
        ✔ Consistencia total
        """

        if not self._pedidos:
            self._estado_pedidos = "generado"
            return

        estados = [p.estado_pedido for p in self._pedidos]

        # PRIORIDAD DE ESTADOS (lógica empresarial)
        if all(e == "finalizado" for e in estados):
            self._estado_pedidos = "finalizado"

        elif all(e in ("entregado", "finalizado") for e in estados):
            self._estado_pedidos = "entregado"

        elif any(e in ("en_transporte", "en_reparto") for e in estados):
            self._estado_pedidos = "en_transporte"

        elif any(e == "en_recogida" for e in estados):
            self._estado_pedidos = "en_transporte"

        else:
            self._estado_pedidos = "generado"

    # ======================================================
    # OPERADOR +=
    # ======================================================
    def __iadd__(self, pedido):
        """
        Añade un pedido al grupo.

        🔥 AUTOMÁTICO:
        - Enlaza pedido con grupo
        - Actualiza estado del grupo
        """

        if not isinstance(pedido, Pedido):
            raise TypeError("Solo Pedido")

        self._pedidos.append(pedido)

        # 🔥 ENLACE REACTIVO
        pedido.set_grupo(self)

        # 🔥 ACTUALIZACIÓN AUTOMÁTICA
        self.actualizar_estado()

        return self

    # ======================================================
    # PROPIEDADES
    # ======================================================
    @property
    def estado_pedidos(self):
        return self._estado_pedidos

    @property
    def pedidos(self):
        return self._pedidos

    def __len__(self):
        return len(self._pedidos)


# ==========================================================
# CLASES DERIVADAS
# ==========================================================
class GrupoRecogida(GrupoPedidos):

    _contador = 0

    def __init__(self):
        super().__init__()
        GrupoRecogida._contador += 1
        self._id = f"GR{GrupoRecogida._contador}"


class GrupoTransporte(GrupoPedidos):

    _contador = 0

    def __init__(self):
        super().__init__()
        GrupoTransporte._contador += 1
        self._id = f"GT{GrupoTransporte._contador}"


class GrupoReparto(GrupoPedidos):

    _contador = 0

    def __init__(self):
        super().__init__()
        GrupoReparto._contador += 1
        self._id = f"GD{GrupoReparto._contador}"