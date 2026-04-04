"""
PERSISTENCIA DE DIRECCIONES
"""

import json
import os

from utiles.utils import encontrar_raiz
from clases.direccion import Direccion


# ==========================================================
# GUARDAR
# ==========================================================

def guardar_direcciones(direcciones):

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", "direcciones.json")

    data = []

    for d in direcciones:

        data.append({
            "pais": d.pais,
            "provincia": d.provincia,
            "ciudad": d.ciudad,
            "calle": d.calle,
            "numero": d.numero,
            "coordenadas": d.coordenadas
        })

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✔ Direcciones guardadas en {ruta}")


# ==========================================================
# CARGAR
# ==========================================================

def cargar_direcciones():

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", "direcciones.json")

    if not os.path.exists(ruta):
        print("❌ No existe fichero de direcciones")
        return []

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    direcciones = []

    for item in data:

        d = Direccion(
            item["pais"],
            item["provincia"],
            item["ciudad"],
            item["calle"],
            item["numero"]
        )

        #  IMPORTANTE → NO llamar geopy
        if item["coordenadas"]:
            d._coordenadas = tuple(item["coordenadas"]) if item["coordenadas"] else None
            # d.coordenadas = tuple(item["coordenadas"])

        direcciones.append(d)

    return direcciones