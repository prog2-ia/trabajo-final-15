# ==========================================================
# VISUALIZAR RUTAS
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

from programas import utils_rutas as rutas

from persistencia.persistencia_rutas import (
    cargar_rutas
)

from persistencia.persistencia_pedidos import (
    cargar_pedidos
)

from persistencia.persistencia_clientes import (
    cargar_clientes
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)


# ==========================================================
# VISUALIZAR RUTA GUARDADA
# ==========================================================
def visualizar_ruta_guardada():

    datos_rutas = cargar_rutas()

    pedidos = cargar_pedidos()

    clientes = cargar_clientes()

    delegaciones = cargar_delegaciones()

    print("\n")
    print("=" * 100)
    print(" RUTAS ACTIVAS ")
    print("=" * 100)

    rutas_validas = {}

    # ======================================================
    # CABECERA
    # ======================================================
    print(
        f"{'Ruta':<8}"
        f"{'Delegación':<25}"
        f"{'Tipo':<15}"
        f"{'Vehículo':<18}"
        f"{'Pedidos':<10}"
        f"{'Peso':<12}"
        f"{'Volumen':<12}"
        f"{'Distancia':<14}"
        f"{'Estado':<12}"
        f"{'Ruta óptima'}"
    )

    print("-" * 200)

    # ======================================================
    # RUTAS
    # ======================================================
    for rid, ruta in datos_rutas.items():

        tipo = str(
            ruta.get("tipo", "")
        ).lower().strip()

        if tipo != "recogida":
            continue

        rutas_validas[rid] = ruta

        delegacion = ruta.get(
            "delegacion",
            "Delegación"
        )

        recorrido = (
                f"{delegacion} -> "
                +
                " -> ".join(ruta["lista_pedidos"])
                +
                f" -> {delegacion}"
        )

        estado = (
            "FINALIZADA"
            if ruta.get("finalizada", False)
            else "ACTIVA"
        )

        print(
            f"{rid:<8}"
            f"{ruta.get('delegacion', 'N/A'):<25}"
            f"{ruta.get('tipo', 'N/A'):<15}"
            f"{ruta.get('vehiculo', 'N/A'):<18}"
            f"{len(ruta['lista_pedidos']):<10}"
            f"{ruta.get('peso_total', 0):<12.2f}"
            f"{ruta.get('volumen_total', 0):<12.2f}"
            f"{ruta['distancia_total']:<14.2f}"
            f"{estado:<12}"
            f"{recorrido}"
        )

        print("-" * 200)

    # ======================================================
    # VALIDACIÓN
    # ======================================================
    if not rutas_validas:

        print(
            "\n❌ No existen rutas"
        )

        return

    # ======================================================
    # SELECCIÓN
    # ======================================================
    ruta_id = input(
        "\nNúmero de ruta: "
    ).strip()

    if ruta_id not in rutas_validas:

        print(
            "\n❌ Ruta inválida"
        )

        return

    ruta = rutas_validas[ruta_id]

    # ======================================================
    # BUSCAR DESPACHO
    # ======================================================
    despacho = None

    for d in delegaciones:

        if (
                d.nombre.lower().strip()
                ==
                ruta["delegacion"].lower().strip()
        ):

            despacho = d
            break

    if not despacho:

        print(
            "\n❌ Delegación no encontrada"
        )

        return

    # ======================================================
    # RECONSTRUIR RUTA
    # ======================================================
    ruta_optima = ["DESPACHO"]

    for pid in ruta["lista_pedidos"]:

        ruta_optima.append(pid)

    ruta_optima.append("DESPACHO")

    # ======================================================
    # VISUALIZAR MAPA
    # ======================================================
    rutas.visualizar_ruta_mapa(

        ruta_optima=ruta_optima,

        pedidos=pedidos,

        clientes=clientes,

        despacho=despacho,

        nombre_fichero="ruta.html"
    )


# ==========================================================
# EJECUTAR
# ==========================================================
def ejecutar():

    visualizar_ruta_guardada()


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    ejecutar()