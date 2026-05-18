# ==========================================================
# GENERAR RUTA DESPACHO
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

from clases.delegacion import DelegacionDespacho

from persistencia.persistencia_clientes import (
    cargar_clientes
)

from persistencia.persistencia_pedidos import (
    cargar_pedidos
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)

from persistencia.persistencia_vehiculos import (
    cargar_vehiculos
)

from programas.utils_rutas import *


def ejecutar():

    delegaciones = cargar_delegaciones()

    clientes = cargar_clientes()

    pedidos = cargar_pedidos()

    vehiculos = cargar_vehiculos()

    print("\nDESPACHOS DISPONIBLES:\n")

    despachos = []

    for d in delegaciones:

        if isinstance(d, DelegacionDespacho):

            despachos.append(d)

            print(d.nombre)

    numero = input(
        "\nNúmero despacho: "
    ).strip()

    despacho = buscar_despacho(
        f"Despacho {numero}",
        delegaciones
    )

    if not despacho:

        print("\n❌ Despacho incorrecto")

        return

    pedidos_filtrados = (
        obtener_pedidos_despacho(
            despacho,
            pedidos,
            clientes
        )
    )

    if not pedidos_filtrados:

        print("\n❌ No hay pedidos")

        return

    mostrar_pedidos_generados(
        pedidos_filtrados,
        clientes
    )

    vehiculos_disponibles = (
        mostrar_vehiculos_disponibles(
            despacho,
            vehiculos
        )
    )

    vehiculo = None

    while vehiculo is None:

        matricula = input(
            "\nVehículo: "
        ).strip().upper()

        for v in vehiculos_disponibles:

            if v.matricula.upper() == matricula:

                vehiculo = v
                break

    while True:

        entrada = input(
            "\nPedidos "
            "(coma separados o TODOS): "
        ).strip().lower()

        if entrada == "todos":

            pedidos_ruta = dict(
                pedidos_filtrados
            )

        else:

            pedidos_ruta = {}

            error = False

            for pid in entrada.split(","):

                pid = pid.strip()

                if pid not in pedidos_filtrados:

                    print(
                        f"❌ Pedido incorrecto: {pid}"
                    )

                    error = True

                else:

                    pedidos_ruta[pid] = (
                        pedidos_filtrados[pid]
                    )

            if error:
                continue

        peso_total = sum(
            p["peso"]
            for p in pedidos_ruta.values()
        )

        volumen_total = sum(
            p["volumen"]
            for p in pedidos_ruta.values()
        )

        if peso_total > vehiculo.carga_maxima:

            print("\n❌ Peso excesivo")

            continue

        if volumen_total > vehiculo.cubicaje:

            print("\n❌ Volumen excesivo")

            continue

        break

    G = crear_grafo_ruta(
        despacho,
        pedidos_ruta,
        clientes
    )

    ruta_optima = calcular_ruta_optima(G)

    distancia_total = mostrar_ruta(
        ruta_optima,
        G,
        despacho,
        peso_total,
        volumen_total
    )

    confirmar = input(
        "\n¿Persistir ruta? (s/n): "
    ).strip().lower()

    if confirmar != "s":

        return

    actualizar_pedidos(
        pedidos_ruta.keys(),
        pedidos
    )

    actualizar_clientes(
        pedidos_ruta.keys(),
        pedidos,
        clientes
    )

    actualizar_vehiculo(
        vehiculo
    )

    persistir_ruta(
        despacho,
        vehiculo,
        list(pedidos_ruta.keys()),
        distancia_total,
        peso_total,
        volumen_total
    )

    visualizar_ruta_mapa(
        ruta_optima,
        pedidos_ruta,
        clientes,
        despacho
    )

    print(
        "\n✔ Ruta generada correctamente"
    )