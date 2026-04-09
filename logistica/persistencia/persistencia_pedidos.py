# ==========================================================
# PERSISTENCIA DE PEDIDOS
# ==========================================================
"""
Módulo de persistencia de pedidos.

FUNCIONES:
- obtener_ruta_pedidos(): devuelve la ruta del JSON de pedidos
- cargar_pedidos(): carga todos los pedidos desde disco
- guardar_pedidos(data): guarda completamente el diccionario recibido
- añadir_pedidos(nuevos): fusiona nuevos pedidos con los existentes
- borrar_pedidos(): elimina el fichero de pedidos si existe
"""

import os
import json

from utiles.utils import encontrar_raiz


# ==========================================================
# RUTA
# ==========================================================
def obtener_ruta_pedidos():
    """
    Devuelve la ruta absoluta del fichero pedidos.json
    """
    base_dir = encontrar_raiz()
    return os.path.join(base_dir, "datos", "pedidos.json")


# ==========================================================
# CARGAR PEDIDOS
# ==========================================================
def cargar_pedidos():
    """
    Carga el fichero de pedidos y devuelve un diccionario.

    Si no existe el fichero, devuelve {}.
    """
    ruta = obtener_ruta_pedidos()

    if not os.path.exists(ruta):
        return {}

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# GUARDAR PEDIDOS
# ==========================================================
def guardar_pedidos(data):
    """
    Guarda completamente el diccionario de pedidos recibido.
    """
    ruta = obtener_ruta_pedidos()

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ==========================================================
# AÑADIR PEDIDOS
# ==========================================================
def añadir_pedidos(nuevos):
    """
    Añade pedidos nuevos al fichero existente sin borrar los anteriores.
    """
    pedidos = cargar_pedidos()
    pedidos.update(nuevos)
    guardar_pedidos(pedidos)


# ==========================================================
# BORRAR PEDIDOS
# ==========================================================
def borrar_pedidos():
    """
    Elimina el fichero de pedidos si existe.
    """
    ruta = obtener_ruta_pedidos()

    if os.path.exists(ruta):
        os.remove(ruta)
        return True

    return False