"""
==========================================================
MÓDULO: generar_vehiculos.py
==========================================================

Generación automática de vehículos del sistema logístico.

FUNCIONALIDADES:
✔ Generación automática de vehículos
✔ Asignación automática a delegaciones
✔ Persistencia en fichero de texto
✔ Carga desde fichero
✔ Listado de vehículos

REGLAS:
✔ Central    → 10 camiones
✔ Base       → 5 furgonetas
✔ Despacho   → 3 furgonetas
                 3 motocicletas
                 3 mochilas

✔ Matrículas aleatorias válidas
✔ Mochilas:
    NombreDelegacion-numero

FORMATO PERSISTENCIA:
tipo|matricula|disponible|delegacion
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
    Vehiculo,
    VehiculoCamion,
    VehiculoFurgoneta,
    VehiculoMotocicleta,
    VehiculoMochila
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)

from persistencia.persistencia_vehiculos import (
    guardar_vehiculos,
    cargar_vehiculos
)
from utiles.utils import (
    generar_matricula,
    encontrar_raiz
)
"""
# ==========================================================
# RUTA FICHERO
# ==========================================================
RUTA_VEHICULOS = os.path.join(
    encontrar_raiz(),
    "datos",
    "vehiculos.txt"
)


# ==========================================================
# GUARDAR VEHÍCULOS
# ==========================================================
def guardar_vehiculos(vehiculos):

    os.makedirs(
        os.path.dirname(RUTA_VEHICULOS),
        exist_ok=True
    )

    with open(
            RUTA_VEHICULOS,
            "w",
            encoding="utf-8"
    ) as f:

        for v in vehiculos:

            linea = (
                f"{v.tipo}|"
                f"{v.matricula}|"
                f"{v.disponible}|"
                f"{v.delegacion.nombre}\n"
            )

            f.write(linea)

    print(
        f"\n✔ Vehículos guardados en:"
        f"\n{RUTA_VEHICULOS}"
    )


# ==========================================================
# CARGAR VEHÍCULOS
# ==========================================================
def cargar_vehiculos():

    # ======================================================
    # LIMPIAR REGISTROS EN MEMORIA
    # ======================================================
    Vehiculo._vehiculos.clear()

    Vehiculo.matriculas_existentes.clear()

    # ======================================================
    # VALIDAR FICHERO
    # ======================================================
    if not os.path.exists(RUTA_VEHICULOS):

        print(
            "\n❌ No existe fichero "
            "de vehículos"
        )

        return []

    delegaciones = cargar_delegaciones()

    mapa_delegaciones = {

        d.nombre: d

        for d in delegaciones
    }

    vehiculos = []

    with open(
            RUTA_VEHICULOS,
            "r",
            encoding="utf-8"
    ) as f:

        for linea in f:

            linea = linea.strip()

            if not linea:
                continue

            (
                tipo,
                matricula,
                disponible,
                nombre_delegacion
            ) = linea.split("|")

            disponible = (
                    disponible == "True"
            )

            delegacion = (
                mapa_delegaciones[
                    nombre_delegacion
                ]
            )

            # --------------------------------------------------
            # CREAR VEHÍCULO
            # --------------------------------------------------
            if tipo == "camion":

                v = VehiculoCamion(
                    matricula,
                    disponible,
                    delegacion
                )

            elif tipo == "furgoneta":

                v = VehiculoFurgoneta(
                    matricula,
                    disponible,
                    delegacion
                )

            elif tipo == "motocicleta":

                v = VehiculoMotocicleta(
                    matricula,
                    disponible,
                    delegacion
                )

            else:

                v = VehiculoMochila(
                    matricula,
                    disponible,
                    delegacion
                )

            vehiculos.append(v)

    return vehiculos
"""
# ==========================================================
# GENERAR CAMIONES
# ==========================================================
def generar_camiones(delegacion):

    vehiculos = []

    for _ in range(10):

        v = VehiculoCamion(

            generar_matricula(),

            True,

            delegacion
        )

        vehiculos.append(v)

    return vehiculos


# ==========================================================
# GENERAR FURGONETAS BASE
# ==========================================================
def generar_furgonetas_base(delegacion):

    vehiculos = []

    for _ in range(5):

        v = VehiculoFurgoneta(

            generar_matricula(),

            True,

            delegacion
        )

        vehiculos.append(v)

    return vehiculos


# ==========================================================
# GENERAR VEHÍCULOS DESPACHO
# ==========================================================
def generar_vehiculos_despacho(delegacion):

    vehiculos = []

    # ------------------------------------------------------
    # FURGONETAS
    # ------------------------------------------------------
    for _ in range(3):

        v = VehiculoFurgoneta(

            generar_matricula(),

            True,

            delegacion
        )

        vehiculos.append(v)

    # ------------------------------------------------------
    # MOTOCICLETAS
    # ------------------------------------------------------
    for _ in range(3):

        v = VehiculoMotocicleta(

            generar_matricula(),

            True,

            delegacion
        )

        vehiculos.append(v)

    # ------------------------------------------------------
    # MOCHILAS
    # ------------------------------------------------------
    nombre = (
        delegacion.nombre
        .replace(" ", "")
    )

    for i in range(1, 4):

        matricula = (
            f"{nombre}-{i}"
        )

        v = VehiculoMochila(

            matricula,

            True,

            delegacion
        )

        vehiculos.append(v)

    return vehiculos


# ==========================================================
# GENERACIÓN GENERAL
# ==========================================================
def generar_vehiculos():

    print("\n" + "=" * 60)
    print("GENERACIÓN DE VEHÍCULOS")
    print("=" * 60)

    # ======================================================
    # LIMPIAR REGISTROS
    # ======================================================
    Vehiculo._vehiculos.clear()

    Vehiculo.matriculas_existentes.clear()

    # ======================================================
    # CARGAR DELEGACIONES
    # ======================================================
    delegaciones = cargar_delegaciones()

    if not delegaciones:

        print(
            "\n❌ No existen delegaciones"
        )

        return

    vehiculos = []

    # ======================================================
    # GENERAR POR TIPO
    # ======================================================
    for d in delegaciones:

        # --------------------------------------------------
        # CENTRAL
        # --------------------------------------------------
        if isinstance(
                d,
                DelegacionCentral
        ):

            nuevos = generar_camiones(d)

        # --------------------------------------------------
        # BASE
        # --------------------------------------------------
        elif isinstance(
                d,
                DelegacionBase
        ):

            nuevos = generar_furgonetas_base(d)

        # --------------------------------------------------
        # DESPACHO
        # --------------------------------------------------
        else:

            nuevos = generar_vehiculos_despacho(d)

        vehiculos.extend(nuevos)

    # ======================================================
    # GUARDAR
    # ======================================================
    guardar_vehiculos(vehiculos)

    # ======================================================
    # RESUMEN
    # ======================================================
    print("\n✔ Vehículos generados")

    print(
        f"\nTotal vehículos: "
        f"{len(vehiculos)}"
    )

    # ------------------------------------------------------
    # CONTADORES
    # ------------------------------------------------------
    camiones = len([
        v for v in vehiculos
        if v.tipo == "camion"
    ])

    furgonetas = len([
        v for v in vehiculos
        if v.tipo == "furgoneta"
    ])

    motos = len([
        v for v in vehiculos
        if v.tipo == "motocicleta"
    ])

    mochilas = len([
        v for v in vehiculos
        if v.tipo == "mochila"
    ])

    print(f"Camiones     : {camiones}")
    print(f"Furgonetas   : {furgonetas}")
    print(f"Motocicletas : {motos}")
    print(f"Mochilas     : {mochilas}")


# ==========================================================
# LISTAR VEHÍCULOS
# ==========================================================
def listar_vehiculos():

    vehiculos = cargar_vehiculos()

    if not vehiculos:
        return

    print("\n" + "=" * 100)
    print("LISTADO DE VEHÍCULOS")
    print("=" * 100)

    for v in vehiculos:

        print(
            f"{v.tipo:<15}"
            f"{v.matricula:<20}"
            f"{str(v.disponible):<12}"
            f"{v.delegacion.nombre}"
        )

def ejecutar():
    print('Se va a generar el archivo de vehiculos')
    opcion = input('Desea continuar? [S/N]')
    if opcion == 's' or opcion == 'S':
        generar_vehiculos()
        listar_vehiculos()


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()

