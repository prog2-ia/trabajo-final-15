# ==========================================================
# CORREGIR DNIS SIN LETRA
# ==========================================================
# Recorre el fichero clientes.json y:
#
# - Detecta DNIs sin letra
# - Calcula la letra correcta
# - Sustituye la clave del diccionario
# - Mantiene intactos los datos del cliente
#
# ==========================================================

import json
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../..'
        )
    )
)

from utiles.utils import (
    encontrar_raiz,
    generar_dni_real,
    validar_dni_real
)


# ==========================================================
# LETRA DNI
# ==========================================================

def calcular_letra_dni(numero):

    letras = "TRWAGMYFPDXBNJZSQVHLCKE"

    return letras[int(numero) % 23]


# ==========================================================
# RUTA JSON
# ==========================================================

BASE_DIR = encontrar_raiz()

RUTA = os.path.join(
    BASE_DIR,
    "datos",
    "clientes.json"
)


# ==========================================================
# CARGA JSON
# ==========================================================

with open(RUTA, "r", encoding="utf-8") as f:

    data = json.load(f)


# ==========================================================
# CORRECCIÓN
# ==========================================================

nuevos_datos = {}

corregidos = 0

for dni, cliente in data.items():

    dni_original = dni

    # ------------------------------------------------------
    # SI YA ES CORRECTO
    # ------------------------------------------------------

    if validar_dni_real(dni):

        nuevos_datos[dni] = cliente

        continue

    # ------------------------------------------------------
    # SI SOLO TIENE NÚMEROS
    # ------------------------------------------------------

    if dni.isdigit() and len(dni) == 8:

        letra = calcular_letra_dni(dni)

        dni_nuevo = f"{dni}{letra}"

        print(
            f"✔ {dni_original} -> {dni_nuevo}"
        )

        nuevos_datos[dni_nuevo] = cliente

        corregidos += 1

    else:

        print(
            f"⚠️ DNI inválido no corregido: {dni}"
        )

        nuevos_datos[dni] = cliente


# ==========================================================
# GUARDAR JSON
# ==========================================================

with open(RUTA, "w", encoding="utf-8") as f:

    json.dump(
        nuevos_datos,
        f,
        indent=4,
        ensure_ascii=False
    )


# ==========================================================
# FINAL
# ==========================================================

print("\n==============================")
print(f"✔ DNIs corregidos: {corregidos}")
print("==============================")