# ==========================================================
# MÓDULO: persistencia_rutas.py
# ==========================================================
"""
Gestiona la persistencia de rutas logísticas.

RESPONSABILIDADES:
✔ Guardar rutas
✔ Cargar rutas
✔ Generar IDs correlativos
✔ Añadir nuevas rutas
✔ Mantener formato JSON consistente

FORMATO JSON:
{
    "1": {
        "tipo": "recogida",
        "delegacion": "Despacho 12",
        "fecha": "2026-05-11 18:45:00",
        "distancia_total": 14.82,
        "lista_pedidos": ["7", "18", "36"]
    }
}
"""

# ==========================================================
# IMPORTS
# ==========================================================
import json
import os

from utiles.utils import encontrar_raiz


# ==========================================================
# RUTA JSON
# ==========================================================
def obtener_ruta_rutas():

    base_dir = encontrar_raiz()

    return os.path.join(
        base_dir,
        "datos",
        "rutas.json"
    )


# ==========================================================
# CARGAR RUTAS
# ==========================================================
def cargar_rutas():

    ruta = obtener_ruta_rutas()

    if not os.path.exists(ruta):
        return {}

    with open(
            ruta,
            "r",
            encoding="utf-8"
    ) as f:

        return json.load(f)


# ==========================================================
# GUARDAR RUTAS
# ==========================================================
def guardar_rutas(data):

    ruta = obtener_ruta_rutas()

    os.makedirs(
        os.path.dirname(ruta),
        exist_ok=True
    )

    with open(
            ruta,
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            data,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# AÑADIR RUTA
# ==========================================================
def añadir_ruta(id_ruta, datos):

    rutas = cargar_rutas()

    rutas[str(id_ruta)] = datos

    guardar_rutas(rutas)


# ==========================================================
# SIGUIENTE ID
# ==========================================================
def obtener_siguiente_id_ruta():

    rutas = cargar_rutas()

    if not rutas:
        return 1

    ids = [
        int(i)
        for i in rutas.keys()
    ]

    return max(ids) + 1