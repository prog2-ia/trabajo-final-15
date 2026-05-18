"""
==========================================================
MÓDULO: persistencia_delegaciones.py
==========================================================
"""

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
# GUARDAR DELEGACIONES
# ==========================================================
def guardar_delegaciones(
        delegaciones,
        nombre_fichero="delegaciones.json"
):

    BASE_DIR = encontrar_raiz()

    ruta = os.path.join(
        BASE_DIR,
        "datos",
        nombre_fichero
    )

    os.makedirs(
        os.path.dirname(ruta),
        exist_ok=True
    )

    data = []

    # ======================================================
    # SERIALIZACIÓN
    # ======================================================
    for d in delegaciones:

        if isinstance(d, DelegacionCentral):
            tipo = "central"

        elif isinstance(d, DelegacionBase):
            tipo = "base"

        else:
            tipo = "despacho"

        nombre_superior = (
            d.superior.nombre
            if d.superior
            else None
        )

        data.append({

            "nombre": d.nombre,

            "direccion": d.direccion,

            "provincia": d.provincia,

            "poblacion": d.poblacion,

            "tipo": tipo,

            "coordenadas": d.coordenadas,

            "superior": nombre_superior
        })

    # ======================================================
    # GUARDADO
    # ======================================================
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

    print(f"✔ Delegaciones guardadas en: {ruta}")


# ==========================================================
# CARGAR DELEGACIONES
# ==========================================================
def cargar_delegaciones(
        nombre_fichero="delegaciones.json"
):

    # ======================================================
    # LIMPIAR REGISTRO
    # ======================================================
    Delegacion.nombres_registrados.clear()

    # ======================================================
    # RUTA
    # ======================================================
    BASE_DIR = encontrar_raiz()

    ruta = os.path.join(
        BASE_DIR,
        "datos",
        nombre_fichero
    )

    if not os.path.exists(ruta):

        print(
            "❌ No existe fichero de delegaciones"
        )

        return []

    # ======================================================
    # LECTURA JSON
    # ======================================================
    with open(
            ruta,
            "r",
            encoding="utf-8"
    ) as f:

        data = json.load(f)

    # ======================================================
    # FASE 1:
    # CREAR OBJETOS SIN RELACIONES
    # ======================================================
    objetos = {}

    for item in data:

        nombre = item["nombre"]

        direccion = item["direccion"]

        provincia = item.get(
            "provincia",
            ""
        )

        poblacion = item.get(
            "poblacion",
            ""
        )

        tipo = item["tipo"]

        coords = item.get(
            "coordenadas"
        )

        coordenadas = (
            tuple(coords)
            if coords
            else None
        )

        # --------------------------------------------------
        # CREAR OBJETO
        # --------------------------------------------------
        if tipo == "central":

            d = DelegacionCentral(
                nombre=nombre,
                direccion=direccion,
                coordenadas=coordenadas,
                provincia_inicial=provincia,
                poblacion_inicial=poblacion
            )

        elif tipo == "base":

            d = DelegacionBase(
                nombre=nombre,
                direccion=direccion,
                coordenadas=coordenadas,
                provincia_inicial=provincia,
                poblacion_inicial=poblacion
            )

        else:

            d = DelegacionDespacho(
                nombre=nombre,
                direccion=direccion,
                coordenadas=coordenadas,
                provincia_inicial=provincia,
                poblacion_inicial=poblacion
            )

        objetos[nombre] = d

    # ======================================================
    # FASE 2:
    # RECONSTRUIR JERARQUÍA
    # ======================================================
    for item in data:

        nombre = item["nombre"]

        nombre_superior = item["superior"]

        if nombre_superior:

            objetos[nombre]._superior = (
                objetos[nombre_superior]
            )

    # ======================================================
    # DEVOLVER OBJETOS
    # ======================================================
    return list(objetos.values())