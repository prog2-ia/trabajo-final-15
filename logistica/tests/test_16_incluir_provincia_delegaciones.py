"""
==========================================================
MIGRACIÓN DE PROVINCIAS EN DELEGACIONES
==========================================================

OBJETIVO

Añadir automáticamente el campo "provincia" a todas las
delegaciones existentes a partir de su dirección.

FUNCIONAMIENTO

1. Carga delegaciones desde JSON
2. Extrae provincia desde dirección
3. Actualiza cada objeto
4. Guarda cambios en JSON

IMPORTANTE

Este script SOLO hay que ejecutarlo una vez
==========================================================
"""

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones,
    guardar_delegaciones
)

# =========================
# PROVINCIAS SOPORTADAS
# =========================
MAPA_PROVINCIAS = {
    "valencia": ["valencia", "torrent", "manises", "alboraya", "paiporta"],
    "alicante": ["alicante", "elche", "san vicente", "campello", "sant joan d'alacant"],
    "madrid": ["madrid", "getafe", "fuenlabrada", "alcorcón"],
    "barcelona": ["barcelona", "badalona", "terrassa", "sabadell"],
    "murcia": ["murcia", "lorca", "cartagena"],
    "zaragoza": ["zaragoza", "calatayud", "utebo"],
    "albacete": ["albacete", "hellín", "almansa"],
    "toledo": ["toledo", "talavera", "seseña"]
}
PROVINCIAS = [
    "madrid", "barcelona", "valencia", "alicante",
    "murcia", "zaragoza", "albacete", "toledo"
]


# =========================
# EXTRAER PROVINCIA
# =========================
def extraer_provincia(direccion):
    direccion = direccion.lower()

    for provincia, ciudades in MAPA_PROVINCIAS.items():
        for ciudad in ciudades:
            if ciudad in direccion:
                return provincia

    return None


# =========================
# SCRIPT PRINCIPAL
# =========================
def migrar_provincias():
    print("\n🚀 INICIANDO MIGRACIÓN DE PROVINCIAS...\n")

    delegaciones = cargar_delegaciones()

    actualizadas = 0
    sin_detectar = []

    for d in delegaciones:

        provincia_detectada = extraer_provincia(d.direccion)

        if provincia_detectada:
            d.provincia = provincia_detectada
            actualizadas += 1
            print(f"✔ {d.nombre} → {provincia_detectada}")
        else:
            sin_detectar.append(d.nombre)
            print(f"❌ {d.nombre} → NO DETECTADA")

    # ----------------------------------
    # GUARDAR CAMBIOS
    # ----------------------------------
    guardar_delegaciones(delegaciones)

    # ----------------------------------
    # RESUMEN
    # ----------------------------------
    print("\n==============================")
    print(f"✔ Actualizadas: {actualizadas}")
    print(f"❌ Sin detectar: {len(sin_detectar)}")

    if sin_detectar:
        print("\nDelegaciones sin provincia:")
        for d in sin_detectar:
            print(f"- {d}")

    print("\n✅ MIGRACIÓN COMPLETADA\n")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    migrar_provincias()
