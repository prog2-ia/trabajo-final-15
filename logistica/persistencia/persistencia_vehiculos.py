"""
==========================================================
MÓDULO: persistencia_vehiculos.py
==========================================================

Persistencia de vehículos del sistema logístico.
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os

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

from utiles.utils import (
    encontrar_raiz
)

# ==========================================================
# RUTA
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
        os.path.dirname(
            RUTA_VEHICULOS
        ),
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
                f"{v.delegacion.nombre}|"
                f"{v.carga_maxima}|"
                f"{v.cubicaje}\n"
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

    Vehiculo._vehiculos.clear()

    Vehiculo.matriculas_existentes.clear()

    if not os.path.exists(
            RUTA_VEHICULOS
    ):

        print(
            "\n❌ No existe fichero "
            "de vehículos"
        )

        return []

    delegaciones = (
        cargar_delegaciones()
    )

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
                nombre_delegacion,
                carga_maxima,
                cubicaje
            ) = linea.split("|")

            disponible = (
                    disponible == "True"
            )

            carga_maxima = (
                float(carga_maxima)
            )

            cubicaje = (
                float(cubicaje)
            )

            delegacion = (
                mapa_delegaciones[
                    nombre_delegacion
                ]
            )

            # ==================================================
            # CREAR VEHÍCULO
            # ==================================================
            if tipo == "camion":

                v = VehiculoCamion(
                    matricula,
                    disponible,
                    delegacion,
                    carga_maxima,
                    cubicaje
                )

            elif tipo == "furgoneta":

                v = VehiculoFurgoneta(
                    matricula,
                    disponible,
                    delegacion,
                    carga_maxima,
                    cubicaje
                )

            elif tipo == "motocicleta":

                v = VehiculoMotocicleta(
                    matricula,
                    disponible,
                    delegacion,
                    carga_maxima,
                    cubicaje
                )

            else:

                v = VehiculoMochila(
                    matricula,
                    disponible,
                    delegacion,
                    carga_maxima,
                    cubicaje
                )

            vehiculos.append(v)

    return vehiculos