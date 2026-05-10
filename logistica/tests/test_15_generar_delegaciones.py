"""
==========================================================
MÓDULO: test_15_generar_delegaciones.py
==========================================================

Generación automática de delegaciones logísticas.

ARQUITECTURA:
Central → Bases → Despachos

FUNCIONALIDADES:
✔ Generación jerárquica de delegaciones
✔ Asignación automática de vehículos
✔ Geolocalización
✔ Persistencia JSON
✔ Visualización en mapa
✔ Visualización en árbol
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
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
    generar_mapa,
    encontrar_raiz
)

from utiles.geolocalizacion import (
    geocodificar_lista
)

from datos.direcciones import (
    direcciones_central_txt,
    direcciones_base_txt,
    direcciones_despacho_txt
)

# ==========================================================
# MAPA DE PROVINCIAS
# ==========================================================
MAPA_PROVINCIAS = {

    "valencia": [
        "valencia",
        "torrent",
        "manises",
        "alboraya",
        "paiporta"
    ],

    "alicante": [
        "alicante",
        "elche",
        "san vicente",
        "campello",
        "sant joan d'alacant"
    ],

    "madrid": [
        "madrid",
        "getafe",
        "fuenlabrada",
        "alcorcón"
    ],

    "barcelona": [
        "barcelona",
        "badalona",
        "terrassa",
        "sabadell"
    ],

    "murcia": [
        "murcia",
        "lorca",
        "cartagena"
    ],

    "zaragoza": [
        "zaragoza",
        "calatayud",
        "utebo"
    ],

    "albacete": [
        "albacete",
        "hellín",
        "almansa"
    ],

    "toledo": [
        "toledo",
        "talavera",
        "seseña"
    ]
}


# ==========================================================
# EXTRAER PROVINCIA
# ==========================================================
def extraer_provincia(direccion):

    direccion = direccion.lower()

    for provincia, ciudades in MAPA_PROVINCIAS.items():

        for ciudad in ciudades:

            if ciudad in direccion:
                return provincia.title()

    return "Desconocida"


# ==========================================================
# EXTRAER POBLACIÓN
# ==========================================================
def extraer_poblacion(direccion):

    direccion = direccion.lower()

    for _, ciudades in MAPA_PROVINCIAS.items():

        for ciudad in ciudades:

            if ciudad in direccion:
                return ciudad.title()

    return "Desconocida"


# ==========================================================
# GENERACIÓN DE VEHÍCULOS
# ==========================================================
def poblar_flota(delegacion):

    if isinstance(delegacion, DelegacionCentral):

        for _ in range(2):

            delegacion.anadir_vehiculo(
                VehiculoCamion(
                    generar_matricula()
                )
            )

    else:

        for _ in range(2):

            delegacion.anadir_vehiculo(
                VehiculoFurgoneta(
                    generar_matricula()
                )
            )


# ==========================================================
# BASE MÁS CERCANA
# ==========================================================
def asignar_base(coord, bases):

    return min(
        bases,
        key=lambda b: distancia_km(
            coord,
            b.coordenadas
        )
    )


# ==========================================================
# VISUALIZACIÓN EN ÁRBOL
# ==========================================================
def imprimir_arbol(delegaciones):

    print("\n")
    print("=" * 50)
    print("        RED LOGÍSTICA")
    print("=" * 50)

    central = next(
        d for d in delegaciones
        if isinstance(d, DelegacionCentral)
    )

    print(
        f"\n{central.nombre}"
        f" [{central.provincia}]"
    )

    bases = [
        d for d in delegaciones
        if isinstance(d, DelegacionBase)
    ]

    for b in bases:

        print(
            f"   ├── {b.nombre}"
            f" [{b.provincia}]"
        )

        despachos = [

            d for d in delegaciones

            if isinstance(
                d,
                DelegacionDespacho
            )

            and d.delegacion_superior == b
        ]

        for d in despachos:

            print(
                f"   │     ├── "
                f"{d.nombre}"
                f" [{d.provincia}]"
            )


# ==========================================================
# FUNCIONES MAPA
# ==========================================================
def get_coord(d):
    return d.coordenadas


def get_popup(d):

    return (
        f"{d.nombre}<br>"
        f"{d.poblacion}<br>"
        f"{d.provincia}"
    )


def get_color(d):

    if isinstance(d, DelegacionCentral):
        return "red"

    elif isinstance(d, DelegacionBase):
        return "blue"

    else:
        return "green"


# ==========================================================
# CONTROL REGENERACIÓN
# ==========================================================
def preguntar_regenerar():

    ruta = os.path.join(
        encontrar_raiz(),
        "datos",
        "delegaciones.json"
    )

    if not os.path.exists(ruta):
        return True

    opcion = input(
        "¿Regenerar delegaciones? (s/n): "
    ).lower()

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
    print("   GENERACION DE DELEGACIONES LOGÍSTICAS")
    print("*" * 40)

    regenerar = preguntar_regenerar()

    # ======================================================
    # CARGAR EXISTENTES
    # ======================================================
    if not regenerar:

        delegaciones = cargar_delegaciones()

        imprimir_arbol(delegaciones)

        generar_mapa(
            delegaciones,
            get_coord,
            get_popup,
            get_color,
            nombre_fichero="mapa_delegaciones.html"
        )

        return

    # ======================================================
    # GENERAR NUEVAS
    # ======================================================

    # ======================================================
    # CENTRAL
    # ======================================================
    dir_central = direcciones_central_txt[0]

    prov_central = extraer_provincia(
        dir_central
    )

    pob_central = extraer_poblacion(
        dir_central
    )

    central = DelegacionCentral(

        "Central Madrid",

        dir_central,

        provincia=prov_central,

        poblacion=pob_central
    )

    central.calcular_coordenadas()

    poblar_flota(central)

    # ======================================================
    # BASES
    # ======================================================
    bases = []

    for i, txt in enumerate(
            direcciones_base_txt
    ):

        prov = extraer_provincia(txt)

        pob = extraer_poblacion(txt)

        b = DelegacionBase(

            f"Base {i + 1}",

            txt,

            delegacion_superior=central,

            provincia=prov,

            poblacion=pob
        )

        b.calcular_coordenadas()

        poblar_flota(b)

        bases.append(b)

    # ======================================================
    # DESPACHOS
    # ======================================================
    coords_despachos, fallidas = (
        geocodificar_lista(
            direcciones_despacho_txt
        )
    )

    despachos = []

    for i, (txt, coord) in enumerate(
            coords_despachos.items()
    ):

        base = asignar_base(
            coord,
            bases
        )

        prov = extraer_provincia(txt)

        pob = extraer_poblacion(txt)

        d = DelegacionDespacho(

            f"Despacho {i + 1}",

            txt,

            delegacion_superior=base,

            provincia=prov,

            poblacion=pob
        )

        d._coordenadas = coord

        poblar_flota(d)

        despachos.append(d)

    # ======================================================
    # INFORME GEO
    # ======================================================
    print("\n🔎 GEOLOCALIZACIÓN")

    print(
        f"✔ OK: "
        f"{len(coords_despachos)}"
    )

    print(
        f"❌ Fallidas: "
        f"{len(fallidas)}"
    )

    # ======================================================
    # PERSISTENCIA
    # ======================================================
    todas = (
            [central]
            + bases
            + despachos
    )

    guardar_delegaciones(todas)

    delegaciones = cargar_delegaciones()

    # ======================================================
    # VISUALIZACIÓN
    # ======================================================
    imprimir_arbol(delegaciones)

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