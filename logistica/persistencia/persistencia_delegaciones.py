# ==========================================================
# IMPORTS
# ==========================================================

import json
import os

from clases.delegacion import (
    Delegacion,
    DelegacionCentral,
    DelegacionBase,
    DelegacionDespacho
)
from utiles.utils import encontrar_raiz


# ==========================================================
# GUARDAR
# ==========================================================

def guardar_delegaciones(delegaciones, nombre_fichero="delegaciones.json"):
    BASE_DIR = encontrar_raiz()

    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    data = []

    for d in delegaciones:

        if isinstance(d, DelegacionCentral):
            tipo = "central"
        elif isinstance(d, DelegacionBase):
            tipo = "base"
        else:
            tipo = "despacho"

        nombre_superior = d.delegacion_superior.nombre if d.delegacion_superior else None

        data.append({
            "nombre": d.nombre,
            "direccion": d.direccion,
            "provincia": d.provincia,
            "tipo": tipo,
            "coordenadas": d.coordenadas,  # 🔥 GUARDAR COORDENADAS
            "superior": nombre_superior
        })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✔ Delegaciones guardadas en: {ruta}")


# ==========================================================
# CARGAR
# ==========================================================

def cargar_delegaciones(nombre_fichero="delegaciones.json"):
    # 🔥 LIMPIAR NOMBRES
    Delegacion.nombres_existentes.clear()

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    if not os.path.exists(ruta):
        print("❌ No existe fichero de delegaciones")
        return []

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ======================================================
    # PRIMER PASO: crear objetos sin relaciones
    # ======================================================

    objetos = {}

    for item in data:

        nombre = item["nombre"]
        direccion = item["direccion"]
        provincia = item.get("provincia", None)
        tipo = item["tipo"]

        if tipo == "central":
            d = DelegacionCentral(nombre, direccion, provincia=provincia)
        elif tipo == "base":
            d = DelegacionBase(nombre, direccion, provincia=provincia)
        else:
            d = DelegacionDespacho(nombre, direccion, provincia=provincia)

        # 🔥 RESTAURAR COORDENADAS
        coords = item.get("coordenadas")
        d._coordenadas = tuple(coords) if coords else None

        objetos[nombre] = d

    # ======================================================
    # SEGUNDO PASO: reconstruir jerarquía
    # ======================================================

    for item in data:

        nombre = item["nombre"]
        nombre_superior = item["superior"]

        if nombre_superior:
            objetos[nombre]._delegacion_superior = objetos[nombre_superior]

    return list(objetos.values())
