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


# ==========================================================
# GENERAR CAMIONES
# ==========================================================
def generar_camiones(delegacion):

    vehiculos = []

    for _ in range(10):

        v = VehiculoCamion(

            generar_matricula(),

            True,

            delegacion,

            carga_maxima=20000,

            cubicaje=40000
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

            delegacion,

            carga_maxima=3500,

            cubicaje=10000
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

            delegacion,

            carga_maxima=1000,

            cubicaje=4000
        )

        vehiculos.append(v)

    # ------------------------------------------------------
    # MOTOCICLETAS
    # ------------------------------------------------------
    for _ in range(3):

        v = VehiculoMotocicleta(

            generar_matricula(),

            True,

            delegacion,

            carga_maxima=30,

            cubicaje=30
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

            delegacion,

            carga_maxima=30,

            cubicaje=30
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

    print("\n" + "=" * 140)
    print("LISTADO DE VEHÍCULOS")
    print("=" * 140)

    # ======================================================
    # CABECERA
    # ======================================================
    print(
        f"{'TIPO':<15}"
        f"{'MATRICULA':<20}"
        f"{'DISPONIBLE':<12}"
        f"{'CARGA MAX':<15}"
        f"{'CUBICAJE':<15}"
        f"{'DELEGACION'}"
    )

    print("-" * 140)

    # ======================================================
    # DATOS
    # ======================================================
    for v in vehiculos:

        print(
            f"{v.tipo:<15}"
            f"{v.matricula:<20}"
            f"{str(v.disponible):<12}"
            f"{str(v.carga_maxima):<15}"
            f"{str(v.cubicaje):<15}"
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