# ==========================================================
# GENERACIÓN DE RUTAS DE RECOGIDA
# ==========================================================

"""
Sistema completo de generación de rutas óptimas
de recogida mediante algoritmo TSP.

FUNCIONALIDAD:
✔ Selección de despacho
✔ Filtrado de pedidos pendientes
✔ Cálculo de distancias
✔ Optimización de recorrido
✔ Persistencia de rutas
✔ Actualización de estados
✔ Actualización de clientes
✔ Visualización de rutas en mapa
✔ Visualización posterior de rutas guardadas
"""

# ==========================================================
# IMPORTS
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

from persistencia.persistencia_clientes import (
    cargar_clientes,
    guardar_clientes
)

from persistencia.persistencia_pedidos import (
    cargar_pedidos,
    guardar_pedidos
)

from persistencia.persistencia_delegaciones import (
    cargar_delegaciones
)

from persistencia.persistencia_rutas import (
    añadir_ruta,
    obtener_siguiente_id_ruta,
    cargar_rutas
)
from persistencia.persistencia_vehiculos import (
    cargar_vehiculos,
    guardar_vehiculos
)


from clases.delegacion import (
    DelegacionDespacho
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
# OBTENER PEDIDOS DEL DESPACHO
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

        cliente_origen = clientes.get(
            p["origen"]
        )

        if not cliente_origen:
            continue

        delegacion = (
            cliente_origen.delegacion_cercana
        )

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
# MOSTRAR RESULTADOS
# ==========================================================
def mostrar_ruta(
        ruta_optima,
        G,
        pedidos,
        clientes,
        despacho
):

    print("\n")
    print("=" * 60)
    print(" RUTA ÓPTIMA DE RECOGIDA ")
    print("=" * 60)

    total = 0

    for i in range(len(ruta_optima) - 1):

        origen = ruta_optima[i]
        destino = ruta_optima[i + 1]

        distancia = G[origen][destino]["weight"]

        total += distancia

        if origen == "DESPACHO":

            txt_origen = despacho.nombre

        else:

            cliente = clientes[
                pedidos[origen]["origen"]
            ]

            txt_origen = (
                f"{cliente.nombre} "
                f"{cliente.apellidos}"
            )

        if destino == "DESPACHO":

            txt_destino = despacho.nombre

        else:

            cliente = clientes[
                pedidos[destino]["origen"]
            ]

            txt_destino = (
                f"{cliente.nombre} "
                f"{cliente.apellidos}"
            )

        print(
            f"{txt_origen}"
            f"  -->  "
            f"{txt_destino}"
            f"   ({distancia:.2f} km)"
        )

    print("-" * 60)

    print(
        f"TOTAL RUTA: "
        f"{total:.2f} km"
    )

    return round(total, 2)


# ==========================================================
# VISUALIZAR MAPA
# ==========================================================
def visualizar_ruta_mapa(
        ruta_optima,
        pedidos,
        clientes,
        despacho,
        nombre_fichero
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

    # ======================================================
    # DESPACHO
    # ======================================================
    folium.Marker(

        location=despacho.coordenadas,

        popup=(
            f"<b>DESPACHO</b><br>"
            f"{despacho.nombre}<br>"
            f"{despacho.direccion}"
        ),

        icon=folium.Icon(
            color="red",
            icon="home"
        )

    ).add_to(mapa)

    # ======================================================
    # RUTA
    # ======================================================
    coordenadas_linea = [
        despacho.coordenadas
    ]

    contador = 1

    for nodo in ruta_optima:

        if nodo == "DESPACHO":
            continue

        pedido = pedidos[nodo]

        cliente = clientes[
            pedido["origen"]
        ]

        coord = cliente.coordenadas

        coordenadas_linea.append(coord)

        # ==================================================
        # MARCADOR
        # ==================================================
        folium.Marker(

            location=coord,

            popup=(
                f"<b>PARADA {contador}</b><br>"
                f"<b>Pedido:</b> {nodo}<br>"
                f"{cliente.nombre} "
                f"{cliente.apellidos}<br>"
                f"{cliente.direccion}"
            ),

            icon=folium.Icon(
                color="blue",
                icon="truck"
            )

        ).add_to(mapa)

        # ==================================================
        # NUMERACIÓN VISUAL
        # ==================================================
        folium.Marker(

            location=coord,

            icon=folium.DivIcon(
                html=f"""
                <div style="
                    font-size: 14px;
                    font-weight: bold;
                    color: black;
                    background-color: white;
                    border-radius: 12px;
                    border: 2px solid black;
                    width: 28px;
                    height: 28px;
                    text-align: center;
                    line-height: 24px;
                ">
                    {contador}
                </div>
                """
            )

        ).add_to(mapa)

        contador += 1

    # ======================================================
    # VOLVER AL DESPACHO
    # ======================================================
    coordenadas_linea.append(
        despacho.coordenadas
    )

    # ======================================================
    # POLYLINE
    # ======================================================
    folium.PolyLine(
        coordenadas_linea,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(mapa)

    # ======================================================
    # GUARDAR MAPA
    # ======================================================
    mapa.save(ruta_html)

    print(
        f"\n✔ Ruta visualizada:"
    )

    print(ruta_html)

    # ======================================================
    # ABRIR MAPA
    # ======================================================
    try:

        subprocess.run(
            ["open", ruta_html]
        )

    except:

        print(
            "⚠️ No se pudo abrir automáticamente"
        )


# ==========================================================
# ACTUALIZAR PEDIDOS
# ==========================================================
def actualizar_pedidos(
        ruta_optima,
        pedidos
):

    pedidos_ruta = []

    for nodo in ruta_optima:

        if nodo == "DESPACHO":
            continue

        pedidos[nodo]["estado"] = "en_recogida"

        pedidos_ruta.append(nodo)

    guardar_pedidos(pedidos)

    return pedidos_ruta


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
# PERSISTIR RUTA
# ==========================================================
# ==========================================================
# PERSISTIR RUTA
# ==========================================================
def persistir_ruta(
        despacho,
        pedidos_ruta,
        distancia_total
):

    id_ruta = obtener_siguiente_id_ruta()

    ruta = Ruta(
        id_ruta=id_ruta,
        delegacion=despacho.nombre,
        tipo_ruta="recogida",
        distancia=distancia_total
    )

    # ======================================================
    # AÑADIR PEDIDOS
    # ======================================================
    for pid in pedidos_ruta:

        ruta.lista_pedidos.append(pid)

    # ======================================================
    # DATOS JSON
    # ======================================================
    datos = {

        "tipo": ruta.tipo_ruta,

        "delegacion": ruta.delegacion,

        "fecha": str(
            ruta.fecha_creacion
        ),

        "distancia_total": ruta.distancia_total,

        "lista_pedidos": ruta.lista_pedidos
    }

    # ======================================================
    # PERSISTIR
    # ======================================================
    añadir_ruta(
        id_ruta,
        datos
    )

    print(
        f"\n✔ Ruta guardada "
        f"correctamente "
        f"(ID {id_ruta})"
    )

    return str(id_ruta)

# ==========================================================
# VISUALIZAR RUTA GUARDADA
# ==========================================================
def visualizar_ruta_guardada():

    rutas = cargar_rutas()

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
    for rid, ruta in rutas.items():

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

    if not rutas_validas:

        print(
            "\n❌ No existen rutas"
        )

        return

    ruta_id = input(
        "\nNúmero de ruta: "
    ).strip()

    if ruta_id not in rutas_validas:

        print(
            "\n❌ Ruta inválida"
        )

        return

    ruta = rutas_validas[ruta_id]

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

    ruta_optima = ["DESPACHO"]

    for pid in ruta["lista_pedidos"]:

        ruta_optima.append(pid)

    ruta_optima.append("DESPACHO")

    visualizar_ruta_mapa(

        ruta_optima=ruta_optima,

        pedidos=pedidos,

        clientes=clientes,

        despacho=despacho,

        nombre_fichero="ruta.html"
    )

# ==========================================================
# GENERAR NUEVA RUTA
# ==========================================================
def generar_ruta():

    delegaciones = cargar_delegaciones()

    clientes = cargar_clientes()

    pedidos = cargar_pedidos()

    print("\nDESPACHOS DISPONIBLES:\n")

    print("-" * 140)
    print(f"{'DESPACHO':<35} {'DIRECCIÓN':<80} {'PEDIDOS':<10}")
    print("-" * 140)

    despachos_con_pedidos = []

    for d in delegaciones:

        if not isinstance(d, DelegacionDespacho):
            continue

        total_pedidos_generados = 0

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
                    d.nombre.lower().strip()
            ):

                total_pedidos_generados += 1

        if total_pedidos_generados > 0:

            despachos_con_pedidos.append(d)

            direccion = (
                d.direccion
                if d.direccion
                else "SIN DIRECCIÓN"
            )

            print(
                f"{d.nombre:<35} "
                f"{direccion:<80} "
                f"{total_pedidos_generados:<10}"
            )

    print("-" * 140)

    if not despachos_con_pedidos:

        print(
            "\n❌ No existen despachos "
            "con pedidos en estado GENERADO.\n"
        )

        return

    nombre = input(
        "\nDespacho: "
    )

    despacho = buscar_despacho(
        nombre,
        delegaciones
    )

    if not despacho:

        print(
            "❌ Despacho no válido"
        )

        return

    pedidos_filtrados = (
        obtener_pedidos_despacho(
            despacho,
            pedidos,
            clientes
        )
    )

    if not pedidos_filtrados:

        print(
            "\n❌ No existen pedidos "
            "pendientes para ese despacho"
        )

        return

    print(
        f"\n✔ Pedidos encontrados: "
        f"{len(pedidos_filtrados)}"
    )

    G = crear_grafo_ruta(
        despacho,
        pedidos_filtrados,
        clientes
    )

    ruta_optima = (
        traveling_salesman_problem(
            G,
            cycle=True,
            weight="weight"
        )
    )

    distancia_total = mostrar_ruta(
        ruta_optima,
        G,
        pedidos_filtrados,
        clientes,
        despacho
    )

    confirmar = input(
        "\n¿Persistir ruta? (s/n): "
    ).lower()

    if confirmar != "s":

        print(
            "\n❌ Operación cancelada"
        )

        return

    pedidos_ruta = actualizar_pedidos(
        ruta_optima,
        pedidos
    )

    actualizar_clientes(
        pedidos_ruta,
        pedidos,
        clientes
    )

    id_ruta = persistir_ruta(
        despacho,
        pedidos_ruta,
        distancia_total
    )

    # ======================================================
    # VISUALIZAR MAPA
    # ======================================================
    visualizar_ruta_mapa(

        ruta_optima=ruta_optima,

        pedidos=pedidos_filtrados,

        clientes=clientes,

        despacho=despacho,

        nombre_fichero=(
            # f"ruta_{id_ruta}.html"
            f"ruta.html"
        )
    )

    print(
        "\n✔ Ruta generada correctamente"
    )

def recoger_pedidos():

    delegaciones = cargar_delegaciones()

    rutas = cargar_rutas()

    pedidos = cargar_pedidos()

    cargar_vehiculos()


    # ======================================================
    # FILTRAR RUTAS ACTIVAS
    # ======================================================
    rutas_activas = {}

    for rid, r in rutas.items():

        if (
                r["tipo"].lower() == "recogida"
                and
                not r.get("finalizada", False)
        ):

            rutas_activas[rid] = r

    # ======================================================
    # VALIDACIÓN
    # ======================================================
    if not rutas_activas:

        print("\n❌ No existen rutas activas")

        return

    # ======================================================
    # MOSTRAR RUTAS ACTIVAS
    # ======================================================
    print("\n")
    print("=" * 180)
    print(" RUTAS ACTIVAS ")
    print("=" * 180)

    print(
        f"{'Ruta':<10}"
        f"{'Delegación':<25}"
        f"{'Vehículo':<20}"
        f"{'Pedidos'}"
    )

    print("-" * 180)

    for rid, r in rutas_activas.items():

        print(
            f"{rid:<10}"
            f"{r['delegacion']:<25}"
            f"{r.get('vehiculo', 'N/A'):<20}"
            f"{', '.join(r['lista_pedidos'])}"
        )

    # ======================================================
    # SELECCIÓN RUTA
    # ======================================================
    ruta = None

    ruta_id = None

    while ruta is None:

        ruta_id = input(
            "\nNúmero ruta: "
        ).strip()

        if ruta_id not in rutas_activas:

            print("❌ Ruta incorrecta")

            continue

        ruta = rutas_activas[ruta_id]

    # ======================================================
    # MOSTRAR PEDIDOS
    # ======================================================
    print("\n")
    print("=" * 80)
    print(" PEDIDOS DE LA RUTA ")
    print("=" * 80)

    for pid in ruta["lista_pedidos"]:

        estado = pedidos[pid]["estado"]

        print(
            f"Pedido {pid} | "
            f"Estado: {estado}"
        )

    # ======================================================
    # PEDIDOS RECOGIDOS
    # ======================================================
    pedidos_recogidos = None

    while pedidos_recogidos is None:

        entrada = input(
            "\nPedidos recogidos "
            "(coma separados o 'todos'): "
        ).strip().lower()

        # --------------------------------------------------
        # TODOS
        # --------------------------------------------------
        if entrada == "todos":

            pedidos_recogidos = list(
                ruta["lista_pedidos"]
            )

            break

        # --------------------------------------------------
        # VALIDAR LISTA
        # --------------------------------------------------
        lista = []

        error = False

        for x in entrada.split(","):

            pid = x.strip()

            if pid not in ruta["lista_pedidos"]:

                print(
                    f"❌ Pedido incorrecto: {pid}"
                )

                error = True

            else:

                lista.append(pid)

        if error:

            continue

        pedidos_recogidos = lista

    # ======================================================
    # CONFIRMACIÓN
    # ======================================================
    confirmar = input(
        "\n¿Confirmar recogida? (s/n): "
    ).strip().lower()

    if confirmar != "s":

        print("\n❌ Operación cancelada")

        return
    # ======================================================
    # ACTUALIZAR ESTADO PEDIDOS RECOGIDOS
    # ======================================================
    nombre_delegacion = (
        ruta["delegacion"]
        .lower()
        .replace(" ", "_")
    )

    for pid in pedidos_recogidos:
        pedidos[pid]["estado"] = (
            f"en_delegacion_{nombre_delegacion}"
        )

    # ======================================================
    # ELIMINAR PEDIDOS DE LA RUTA
    # ======================================================
    pedidos_restantes = []

    for pid in ruta["lista_pedidos"]:

        if pid not in pedidos_recogidos:
            pedidos_restantes.append(pid)

    ruta["lista_pedidos"] = pedidos_restantes
    # ======================================================
    # SI QUEDAN PEDIDOS
    # ======================================================
    if pedidos_restantes:

        print("\n")
        print("=" * 80)
        print(" PEDIDOS PENDIENTES ")
        print("=" * 80)

        for pid in pedidos_restantes:

            print(f"Pedido {pid}")

        finalizar = input(
            "\n¿Marcar ruta como finalizada? (s/n): "
        ).strip().lower()

        if finalizar == "s":

            # ==============================================
            # MARCAR RUTA FINALIZADA
            # ==============================================
            ruta["finalizada"] = True

            # ==============================================
            # LIBERAR VEHÍCULO
            # ==============================================
            matricula = ruta["vehiculo"]

            for v in Vehiculo.vehiculos_registrados():

                if v.matricula == matricula:

                    v.disponible = True
                    break

            guardar_vehiculos(
                Vehiculo.vehiculos_registrados()
            )

            # ==============================================
            # DEVOLVER PEDIDOS A GENERADO
            # ==============================================
            for pid in pedidos_restantes:

                pedidos[pid]["estado"] = "generado"

    # ======================================================
    # SI NO QUEDAN PEDIDOS
    # ======================================================
    else:

        ruta["finalizada"] = True

        matricula = ruta["vehiculo"]

        for v in Vehiculo.vehiculos_registrados():

            if v.matricula == matricula:

                v.disponible = True
                break

        guardar_vehiculos(
            Vehiculo.vehiculos_registrados()
        )

    # ======================================================
    # GUARDAR
    # ======================================================
    guardar_rutas(rutas)

    guardar_pedidos(pedidos)

    print(
        "\n✔ Pedidos recogidos correctamente"
    )


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def ejecutar():

    while True:

        print("\n")
        print("=" * 70)
        print(" GESTIÓN DE RUTAS DE RECOGIDA ")
        print("=" * 70)

        print("1. Generar ruta")
        print("2. Recoger pedidos de ruta")
        print("3. Visualizar rutas")
        print("0. Salir")

        opcion = input(
            "\nOpción: "
        ).strip()

        if opcion == "1":

            generar_ruta()

        elif opcion == "2":

            recoger_pedidos()

        elif opcion == "3":

            visualizar_ruta_guardada()

        elif opcion == "0":

            break

        else:

            print(
                "\n❌ Opción no válida"
            )
# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":

    ejecutar()