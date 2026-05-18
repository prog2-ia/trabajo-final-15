# ==========================================================
# UTILIDADES COMUNES DE RUTAS
# ==========================================================

import os
import sys
import subprocess

import folium
import networkx as nx

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from networkx.algorithms.approximation import (
    traveling_salesman_problem
)

from clases.ruta import Ruta
from clases.vehiculo import Vehiculo
from clases.delegacion import DelegacionDespacho

from persistencia.persistencia_clientes import (
    guardar_clientes
)

from persistencia.persistencia_pedidos import (
    guardar_pedidos
)

from persistencia.persistencia_rutas import (
    añadir_ruta,
    obtener_siguiente_id_ruta
)

from persistencia.persistencia_vehiculos import (
    guardar_vehiculos
)

from utiles.utils import (
    distancia_km,
    encontrar_raiz
)


# ==========================================================
# BUSCAR DESPACHO
# ==========================================================
def buscar_despacho(nombre, delegaciones):

    nombre = nombre.strip().lower()

    for d in delegaciones:

        if (
                isinstance(d, DelegacionDespacho)
                and d.nombre.lower() == nombre
        ):
            return d

    return None


# ==========================================================
# OBTENER PEDIDOS DESPACHO
# ==========================================================
def obtener_pedidos_despacho(
        despacho,
        pedidos,
        clientes
):

    pedidos_filtrados = {}

    for pid, p in pedidos.items():

        estado = str(
            p.get("estado", "")
        ).lower().strip()

        if estado != "generado":
            continue

        cliente = clientes.get(
            p["origen"]
        )

        if not cliente:
            continue

        delegacion = cliente.delegacion_cercana

        if not delegacion:
            continue

        if (
                delegacion.nombre.lower().strip()
                ==
                despacho.nombre.lower().strip()
        ):

            pedidos_filtrados[pid] = p

    return pedidos_filtrados


# ==========================================================
# MOSTRAR PEDIDOS
# ==========================================================
def mostrar_pedidos_generados(
        pedidos_filtrados,
        clientes
):

    print("\n")
    print("=" * 140)
    print(" PEDIDOS GENERADOS ")
    print("=" * 140)

    print(
        f"{'Pedido':<10}"
        f"{'Cliente':<35}"
        f"{'Peso':<12}"
        f"{'Volumen':<12}"
        f"{'Dirección'}"
    )

    print("-" * 140)

    peso_total = 0
    volumen_total = 0

    for pid, p in pedidos_filtrados.items():

        cliente = clientes[p["origen"]]

        peso = float(p["peso"])
        volumen = float(p["volumen"])

        peso_total += peso
        volumen_total += volumen

        print(
            f"{pid:<10}"
            f"{(cliente.nombre + ' ' + cliente.apellidos):<35}"
            f"{peso:<12.2f}"
            f"{volumen:<12.2f}"
            f"{cliente.direccion}"
        )

    print("-" * 140)

    print(f"TOTAL PESO: {peso_total:.2f} kg")
    print(f"TOTAL VOLUMEN: {volumen_total:.2f}")

    return round(peso_total, 2), round(volumen_total, 2)


# ==========================================================
# MOSTRAR VEHÍCULOS
# ==========================================================
def mostrar_vehiculos_disponibles(
        despacho,
        vehiculos
):

    disponibles = []

    print("\n")
    print("=" * 120)
    print(" VEHÍCULOS DISPONIBLES ")
    print("=" * 120)

    print(
        f"{'Matrícula':<20}"
        f"{'Tipo':<15}"
        f"{'Carga máxima':<20}"
        f"{'Volumen máximo'}"
    )

    print("-" * 120)

    for v in vehiculos:

        if (
                v.delegacion.nombre.lower().strip()
                ==
                despacho.nombre.lower().strip()
                and
                v.disponible
        ):

            disponibles.append(v)

            print(
                f"{v.matricula:<20}"
                f"{v.tipo:<15}"
                f"{v.carga_maxima:<20.2f}"
                f"{v.cubicaje:.2f}"
            )

    return disponibles


# ==========================================================
# CREAR GRAFO
# ==========================================================
def crear_grafo_ruta(
        despacho,
        pedidos,
        clientes
):

    G = nx.complete_graph(0)

    G.add_node(
        "DESPACHO",
        coordenadas=despacho.coordenadas
    )

    for pid, p in pedidos.items():

        cliente = clientes[p["origen"]]

        G.add_node(
            pid,
            coordenadas=cliente.coordenadas
        )

    nodos = list(G.nodes())

    for i in range(len(nodos)):

        for j in range(i + 1, len(nodos)):

            n1 = nodos[i]
            n2 = nodos[j]

            c1 = G.nodes[n1]["coordenadas"]
            c2 = G.nodes[n2]["coordenadas"]

            distancia = round(
                distancia_km(c1, c2),
                2
            )

            G.add_edge(
                n1,
                n2,
                weight=distancia
            )

    return G


# ==========================================================
# CALCULAR TSP
# ==========================================================
def calcular_ruta_optima(G):

    return traveling_salesman_problem(
        G,
        cycle=True,
        weight="weight"
    )


# ==========================================================
# MOSTRAR RUTA
# ==========================================================
def mostrar_ruta(
        ruta_optima,
        G,
        despacho,
        peso_total,
        volumen_total
):

    print("\n")
    print("=" * 80)
    print(" RUTA ÓPTIMA ")
    print("=" * 80)

    total_km = 0

    recorrido = []

    for i in range(len(ruta_optima) - 1):

        origen = ruta_optima[i]
        destino = ruta_optima[i + 1]

        distancia = G[origen][destino]["weight"]

        total_km += distancia

        txt_origen = (
            despacho.nombre
            if origen == "DESPACHO"
            else origen
        )

        txt_destino = (
            despacho.nombre
            if destino == "DESPACHO"
            else destino
        )

        recorrido.append(txt_origen)

        print(
            f"{txt_origen} --> "
            f"{txt_destino} "
            f"({distancia:.2f} km)"
        )

    recorrido.append(despacho.nombre)

    print("-" * 80)

    print(
        f"RUTA: {' -> '.join(recorrido)}"
    )

    print(f"KM TOTALES: {total_km:.2f}")
    print(f"PESO TOTAL: {peso_total:.2f} kg")
    print(f"VOLUMEN TOTAL: {volumen_total:.2f}")

    return round(total_km, 2)


# ==========================================================
# VISUALIZAR MAPA
# ==========================================================
def visualizar_ruta_mapa(
        ruta_optima,
        pedidos,
        clientes,
        despacho,
        nombre_fichero="ruta.html"
):

    BASE_DIR = encontrar_raiz()

    ruta_html = os.path.join(
        BASE_DIR,
        "datos",
        nombre_fichero
    )

    mapa = folium.Map(
        location=despacho.coordenadas,
        zoom_start=11
    )

    folium.Marker(
        location=despacho.coordenadas,
        popup=despacho.nombre,
        icon=folium.Icon(
            color="red",
            icon="home"
        )
    ).add_to(mapa)

    coordenadas = [despacho.coordenadas]

    contador = 1

    for nodo in ruta_optima:

        if nodo == "DESPACHO":
            continue

        pedido = pedidos[nodo]

        cliente = clientes[pedido["origen"]]

        coord = cliente.coordenadas

        coordenadas.append(coord)

        folium.Marker(
            location=coord,
            popup=(
                f"Parada {contador}<br>"
                f"Pedido {nodo}"
            ),
            icon=folium.Icon(
                color="blue",
                icon="truck"
            )
        ).add_to(mapa)

        contador += 1

    coordenadas.append(
        despacho.coordenadas
    )

    folium.PolyLine(
        coordenadas,
        color="blue",
        weight=5
    ).add_to(mapa)

    mapa.save(ruta_html)

    try:

        subprocess.run(
            ["open", ruta_html]
        )

    except:

        pass


# ==========================================================
# ACTUALIZAR PEDIDOS
# ==========================================================
def actualizar_pedidos(
        pedidos_ruta,
        pedidos
):

    for pid in pedidos_ruta:

        pedidos[pid]["estado"] = (
            "en_recogida"
        )

    guardar_pedidos(pedidos)


# ==========================================================
# ACTUALIZAR CLIENTES
# ==========================================================
def actualizar_clientes(
        pedidos_ruta,
        pedidos,
        clientes
):

    for pid in pedidos_ruta:

        p = pedidos[pid]

        cliente = clientes.get(
            p["origen"]
        )

        if not cliente:
            continue

        if pid not in cliente._pedidos_en_curso:

            cliente._pedidos_en_curso.append(
                pid
            )

    guardar_clientes(clientes)


# ==========================================================
# ACTUALIZAR VEHÍCULO
# ==========================================================
def actualizar_vehiculo(
        vehiculo
):

    vehiculo.disponible = False

    guardar_vehiculos(
        Vehiculo.vehiculos_registrados()
    )


# ==========================================================
# PERSISTIR RUTA
# ==========================================================
def persistir_ruta(
        despacho,
        vehiculo,
        pedidos_ruta,
        distancia_total,
        peso_total,
        volumen_total
):

    id_ruta = obtener_siguiente_id_ruta()

    ruta = Ruta(
        id_ruta=id_ruta,
        delegacion=despacho.nombre,
        tipo_ruta="recogida",
        distancia=distancia_total,
        vehiculo=vehiculo,
        peso_total=peso_total,
        volumen_total=volumen_total,
        finalizada=False
    )

    ruta.lista_pedidos = list(
        pedidos_ruta
    )

    datos = {

        "tipo": ruta.tipo_ruta,
        "delegacion": ruta.delegacion,
        "fecha": str(ruta.fecha_creacion),
        "distancia_total": ruta.distancia_total,
        "vehiculo": vehiculo.matricula,
        "peso_total": peso_total,
        "volumen_total": volumen_total,
        "finalizada": False,
        "lista_pedidos": ruta.lista_pedidos
    }

    añadir_ruta(
        id_ruta,
        datos
    )

    return str(id_ruta)