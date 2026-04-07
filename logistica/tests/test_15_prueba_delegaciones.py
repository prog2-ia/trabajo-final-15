# ==========================================================
# DESCRIPCIÓN GENERAL DEL PROGRAMA
# ==========================================================
"""
SCRIPT DE TESTING: RED DE DELEGACIONES LOGÍSTICAS

✔ Incluye detección automática de provincia
✔ Persistencia completa
✔ Geolocalización optimizada
✔ Sistema jerárquico validado
"""

# ==========================================================
# IMPORTS
# ==========================================================

import os
import sys

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from clases.delegacion import (
    DelegacionCentral,
    DelegacionBase,
    DelegacionDespacho
)

from clases.vehiculo import (
    VehiculoCamion,
    VehiculoFurgoneta
)

from persistencia.persistencia_delegaciones import (
    guardar_delegaciones,
    cargar_delegaciones
)

from utiles.utils import (
    generar_matricula,
    distancia_km,
    generar_mapa
)
from utiles.geolocalizacion import geocodificar_lista

from datos.direcciones import (
    direcciones_central_txt,
    direcciones_base_txt,
    direcciones_despacho_txt
)

# ==========================================================
# EXTRAER PROVINCIA
# ==========================================================

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


def extraer_provincia(direccion):
    direccion = direccion.lower()

    for provincia, ciudades in MAPA_PROVINCIAS.items():
        for ciudad in ciudades:
            if ciudad in direccion:
                return provincia

    return None


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def poblar_flota(d):
    if isinstance(d, DelegacionCentral):
        for _ in range(2):
            d.flota.añadir_vehiculo(VehiculoCamion(generar_matricula()))
    else:
        for _ in range(2):
            d.flota.añadir_vehiculo(VehiculoFurgoneta(generar_matricula()))


def asignar_base(coord, bases):
    return min(
        bases,
        key=lambda b: distancia_km(coord, b.coordenadas)
    )


def imprimir_arbol(delegaciones):
    print("\n========== RED LOGÍSTICA ==========\n")

    central = next(d for d in delegaciones if isinstance(d, DelegacionCentral))
    print(f"{central.nombre} ({central.direccion}) [{central.provincia}]")

    bases = [d for d in delegaciones if isinstance(d, DelegacionBase)]

    for b in bases:
        print(f"   ├── {b.nombre} ({b.direccion}) [{b.provincia}]")

        despachos = [
            d for d in delegaciones
            if isinstance(d, DelegacionDespacho) and d.delegacion_superior == b
        ]

        for d in despachos:
            print(f"   │     ├── {d.nombre} ({d.direccion}) [{d.provincia}]")


def get_coord(d):
    return d.coordenadas


def get_popup(d):
    return f"{d.nombre}<br>{d.direccion}<br>{d.provincia}"


def get_color(d):
    if isinstance(d, DelegacionCentral):
        return "red"
    elif isinstance(d, DelegacionBase):
        return "blue"
    else:
        return "green"


def preguntar_regenerar():
    from utiles.utils import encontrar_raiz
    import os

    ruta = os.path.join(encontrar_raiz(), "datos", "delegaciones.json")

    if not os.path.exists(ruta):
        return True

    opcion = input("¿Regenerar delegaciones? (s/n): ").lower()

    if opcion == "s":
        os.remove(ruta)
        print("🗑️ Delegaciones eliminadas")
        return True

    print("✔ Usando delegaciones existentes")
    return False


# ==========================================================
# MAIN
# ==========================================================
def ejecutar():
    print("\n" + "*" * 40)
    print("   GENERACION DE DATOS DE PRUEBA DE DELEGACIONES CON GEOLOCALIZACIÓN")
    print("*" * 40)

    print("\n🚀 Iniciando test de delegaciones...\n")

    regenerar = preguntar_regenerar()

    # ==========================================================
    # CASO 1 → USAR EXISTENTES
    # ==========================================================
    if not regenerar:
        delegaciones = cargar_delegaciones()

        print("\n🔎 ESTADO FINAL:\n")
        for d in delegaciones:
            print(f"{d.nombre} → {d.provincia}")

        imprimir_arbol(delegaciones)

        generar_mapa(
            delegaciones,
            get_coord,
            get_popup,
            get_color,
            nombre_fichero="mapa_delegaciones.html"
        )

        return

    # ==========================================================
    # CASO 2 → GENERAR NUEVAS
    # ==========================================================

    # ----------------------------------------------------------
    # CENTRAL
    # ----------------------------------------------------------
    dir_central = direcciones_central_txt[0]
    prov_central = extraer_provincia(dir_central)

    central = DelegacionCentral("Central Madrid", dir_central, provincia=prov_central)

    central.asignar_flota()
    poblar_flota(central)
    central.calcular_coordenadas()

    # ----------------------------------------------------------
    # BASES
    # ----------------------------------------------------------
    bases = []

    for i, txt in enumerate(direcciones_base_txt):
        prov = extraer_provincia(txt)

        b = DelegacionBase(f"Base {i + 1}", txt, central, prov)

        b.asignar_flota()
        poblar_flota(b)
        b.calcular_coordenadas()

        bases.append(b)

    # ----------------------------------------------------------
    # DESPACHOS
    # ----------------------------------------------------------
    coords_despachos, fallidas = geocodificar_lista(direcciones_despacho_txt)

    despachos = []

    for i, (txt, coord) in enumerate(coords_despachos.items()):
        base = asignar_base(coord, bases)
        prov = extraer_provincia(txt)

        d = DelegacionDespacho(f"Despacho {i + 1}", txt, base, prov)

        d.asignar_flota()
        poblar_flota(d)
        d._coordenadas = coord

        despachos.append(d)

    # ----------------------------------------------------------
    # INFORME GEO
    # ----------------------------------------------------------
    print("\n🔎 INFORME DE GEOLOCALIZACIÓN\n")
    print(f"✔ Direcciones válidas: {len(coords_despachos)}")
    print(f"❌ Direcciones fallidas: {len(fallidas)}\n")

    # ----------------------------------------------------------
    # PERSISTENCIA
    # ----------------------------------------------------------
    todas = [central] + bases + despachos
    guardar_delegaciones(todas)

    delegaciones = cargar_delegaciones()

    # ----------------------------------------------------------
    # VERIFICACIÓN
    # ----------------------------------------------------------
    print("\n🔎 ESTADO FINAL:\n")

    for d in delegaciones:
        print(f"{d.nombre} → {d.provincia}")

    # ----------------------------------------------------------
    # ÁRBOL
    # ----------------------------------------------------------
    imprimir_arbol(delegaciones)

    # ----------------------------------------------------------
    # MAPA
    # ----------------------------------------------------------
    generar_mapa(
        delegaciones,
        get_coord,
        get_popup,
        get_color,
        nombre_fichero="mapa_delegaciones.html"
    )


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()
