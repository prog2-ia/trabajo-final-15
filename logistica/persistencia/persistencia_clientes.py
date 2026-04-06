# ==========================================================
# PERSISTENCIA CLIENTES - VERSION FINAL PRO
# ==========================================================

import json
import os

from clases.cliente import Cliente
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.utils import encontrar_raiz

# ==========================================================
# GUARDAR
# ==========================================================
def guardar_clientes(clientes, nombre_fichero="clientes.json"):

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    data = []

    for c in clientes.values():

        data.append({
            "dni": c.dni,
            "nombre": c.nombre,
            "apellidos": c.apellidos,
            "direccion": c.direccion,
            "coordenadas": c.coordenadas,
            "delegacion": c.delegacion_cercana.nombre if c.delegacion_cercana else None,
            "provincia": getattr(c, "_provincia", None)
        })

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✔ Clientes guardados en: {ruta}")


# ==========================================================
# CARGAR
# ==========================================================
def cargar_clientes(nombre_fichero="clientes.json"):

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    if not os.path.exists(ruta):
        return {}

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)



    delegaciones = cargar_delegaciones()
    mapa = {d.nombre: d for d in delegaciones}

    clientes = {}

    for item in data:

        deleg = mapa.get(item.get("delegacion"))

        c = Cliente(
            item.get("dni"),
            item.get("nombre"),
            item.get("apellidos"),
            item.get("direccion"),
            deleg
        )

        c._coordenadas = tuple(item.get("coordenadas")) if item.get("coordenadas") else None
        c._provincia = item.get("provincia")

        clientes[c.dni] = c

    print(f"✔ Clientes cargados: {len(clientes)}")

    return clientes