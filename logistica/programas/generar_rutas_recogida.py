# ==========================================================
# GENERACIÓN DE RUTAS DE RECOGIDA
# ==========================================================

"""
Sistema completo de generación de rutas óptimas
de recogida mediante algoritmo TSP.

FUNCIONALIDAD:
✔ Selección de despacho
✔ Selección de vehículo
✔ Validación de capacidad
✔ Filtrado de pedidos pendientes
✔ Selección manual de pedidos o TODOS
✔ Cálculo de distancias
✔ Optimización de recorrido
✔ Persistencia de rutas
✔ Actualización de estados
✔ Actualización de clientes
✔ Actualización de vehículos
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

from clases.vehiculo import (
    Vehiculo
)

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
    cargar_rutas,
    guardar_rutas
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

    print(
        f"TOTAL PESO: {peso_total:.2f} kg"
    )

    print(
        f"TOTAL VOLUMEN: {volumen_total:.2f}"
    )

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

    print("-" * 120)

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
# MOSTRAR RESULTADOS
# ==========================================================
def mostrar_ruta(
        ruta_optima,
        G,
        pedidos,
        clientes,
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

        if origen == "DESPACHO":

            txt_origen = despacho.nombre

        else:

            txt_origen = origen

        if destino == "DESPACHO":

            txt_destino = despacho.nombre

        else:

            txt_destino = destino

        recorrido.append(txt_origen)

        print(
            f"{txt_origen}"
            f" --> "
            f"{txt_destino}"
            f" ({distancia:.2f} km)"
        )

    recorrido.append(despacho.nombre)

    print("-" * 80)

    print(
        f"RUTA: {' -> '.join(recorrido)}"
    )

    print(
        f"KM TOTALES: {total_km:.2f}"
    )

    print(
        f"PESO TOTAL: {peso_total:.2f} kg"
    )

    print(
        f"VOLUMEN TOTAL: {volumen_total:.2f}"
    )

    return round(total_km, 2)


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

    folium.Marker(

        location=despacho.coordenadas,

        popup=(
            f"<b>DESPACHO</b><br>"
            f"{despacho.nombre}"
        ),

        icon=folium.Icon(
            color="red",
            icon="home"
        )

    ).add_to(mapa)

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

        folium.Marker(

            location=coord,

            popup=(
                f"<b>PARADA {contador}</b><br>"
                f"Pedido: {nodo}<br>"
                f"{cliente.nombre} "
                f"{cliente.apellidos}"
            ),

            icon=folium.Icon(
                color="blue",
                icon="truck"
            )

        ).add_to(mapa)

        contador += 1

    coordenadas_linea.append(
        despacho.coordenadas
    )

    folium.PolyLine(
        coordenadas_linea,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(mapa)

    mapa.save(ruta_html)

    print(f"\n✔ Ruta visualizada:")
    print(ruta_html)

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

    for pid in pedidos_ruta:

        ruta.lista_pedidos.append(pid)

    datos = {

        "tipo": ruta.tipo_ruta,

        "delegacion": ruta.delegacion,

        "fecha": str(
            ruta.fecha_creacion
        ),

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

    print(
        f"\n✔ Ruta guardada "
        f"(ID {id_ruta})"
    )

    return str(id_ruta)
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

    coordenadas_linea = [
        despacho.coordenadas
    ]

    contador = 1

    # ======================================================
    # CLIENTES
    # ======================================================
    for nodo in ruta_optima:

        if nodo == "DESPACHO":
            continue

        pedido = pedidos[nodo]

        cliente = clientes[
            pedido["origen"]
        ]

        coord = cliente.coordenadas

        coordenadas_linea.append(coord)

        # --------------------------------------------------
        # MARCADOR
        # --------------------------------------------------
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

        # --------------------------------------------------
        # NÚMERO VISUAL
        # --------------------------------------------------
        folium.Marker(

            location=coord,

            icon=folium.DivIcon(
                html=f'''
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
                '''
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
    # DIBUJAR RUTA
    # ======================================================
    folium.PolyLine(
        coordenadas_linea,
        color="blue",
        weight=5,
        opacity=0.8
    ).add_to(mapa)

    # ======================================================
    # GUARDAR
    # ======================================================
    mapa.save(ruta_html)

    print(
        f"\n✔ Ruta visualizada:"
    )

    print(ruta_html)

    # ======================================================
    # ABRIR
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

    nombre_delegacion = ruta["delegacion"]

    numero_despacho = (
        nombre_delegacion
        .lower()
        .replace("despacho", "")
        .strip()
    )

    nuevo_estado = (
        f"en_despacho_{numero_despacho}"
    )

    for pid in pedidos_recogidos:

        pedidos[pid]["estado"] = nuevo_estado
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
# GENERAR NUEVA RUTA
# ==========================================================
def generar_ruta():

    delegaciones = cargar_delegaciones()

    clientes = cargar_clientes()

    pedidos = cargar_pedidos()

    vehiculos = cargar_vehiculos()

    print("\nDESPACHOS DISPONIBLES:\n")

    despachos_con_pedidos = []

    for d in delegaciones:

        if not isinstance(d, DelegacionDespacho):
            continue

        total = 0

        for pid, p in pedidos.items():

            if (
                    p["estado"].lower()
                    != "generado"
            ):
                continue

            cliente = clientes.get(
                p["origen"]
            )

            if not cliente:
                continue

            delegacion = (
                cliente.delegacion_cercana
            )

            if (
                    delegacion
                    and
                    delegacion.nombre.lower()
                    ==
                    d.nombre.lower()
            ):

                total += 1

        if total > 0:

            despachos_con_pedidos.append(d)

            print(
                f"{d.nombre:<30}"
                f"Pedidos: {total}"
            )

    if not despachos_con_pedidos:

        print(
            "\n❌ No existen pedidos"
        )

        return

    numero = input(
        "\nNúmero despacho: "
    ).strip()

    nombre_despacho = (
        f"Despacho {numero}"
    )

    despacho = buscar_despacho(
        nombre_despacho,
        delegaciones
    )

    if not despacho:

        print(
            "\n❌ Despacho incorrecto"
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
            "\n❌ No hay pedidos"
        )

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

    if not vehiculos_disponibles:

        print(
            "\n❌ No hay vehículos disponibles"
        )

        return

    vehiculo = None

    while vehiculo is None:

        matricula = input(
            "\nVehículo: "
        ).strip().upper()

        for v in vehiculos_disponibles:

            if v.matricula.upper() == matricula:

                vehiculo = v
                break

        if vehiculo is None:

            print(
                "❌ Vehículo incorrecto"
            )

    # ======================================================
    # SELECCIÓN Y VALIDACIÓN PEDIDOS
    # ======================================================
    while True:

        pedidos_ruta = None

        entrada = input(
            "\nPedidos "
            "(coma separados o TODOS): "
        ).strip().lower()

        # ==================================================
        # TODOS
        # ==================================================
        if entrada == "todos":

            pedidos_ruta = dict(
                pedidos_filtrados
            )

        else:

            lista_ids = [
                x.strip()
                for x in entrada.split(",")
            ]

            error = False

            seleccionados = {}

            for pid in lista_ids:

                if pid not in pedidos_filtrados:

                    print(
                        f"❌ Pedido incorrecto: {pid}"
                    )

                    error = True

                else:

                    seleccionados[pid] = (
                        pedidos_filtrados[pid]
                    )

            if error:
                continue

            pedidos_ruta = seleccionados

        # ==================================================
        # CALCULAR PESO/VOLUMEN
        # ==================================================
        peso_total = sum(
            p["peso"]
            for p in pedidos_ruta.values()
        )

        volumen_total = sum(
            p["volumen"]
            for p in pedidos_ruta.values()
        )

        print("\n")
        print("=" * 60)
        print(" RESUMEN RUTA ")
        print("=" * 60)

        print(
            f"Peso total: "
            f"{peso_total:.2f} kg"
        )

        print(
            f"Volumen total: "
            f"{volumen_total:.2f}"
        )

        print(
            f"Capacidad peso vehículo: "
            f"{vehiculo.carga_maxima:.2f} kg"
        )

        print(
            f"Capacidad volumen vehículo: "
            f"{vehiculo.cubicaje:.2f}"
        )

        # ==================================================
        # VALIDAR CAPACIDAD
        # ==================================================
        if peso_total > vehiculo.carga_maxima:
            print(
                "\n❌ Peso superior "
                "a la capacidad del vehículo"
            )

            print(
                "Seleccione menos pedidos."
            )

            continue

        if volumen_total > vehiculo.cubicaje:
            print(
                "\n❌ Volumen superior "
                "a la capacidad del vehículo"
            )

            print(
                "Seleccione menos pedidos."
            )

            continue

        break


    if volumen_total > vehiculo.cubicaje:

        print(
            "\n❌ Volumen superior "
            "a la capacidad"
        )

        return

    # ======================================================
    # CREAR GRAFO
    # ======================================================
    G = crear_grafo_ruta(
        despacho,
        pedidos_ruta,
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
        pedidos_ruta,
        clientes,
        despacho,
        peso_total,
        volumen_total
    )

    confirmar = input(
        "\n¿Persistir ruta? (s/n): "
    ).strip().lower()

    if confirmar != "s":

        print(
            "\n❌ Operación cancelada"
        )

        return

    # ======================================================
    # ACTUALIZAR PEDIDOS
    # ======================================================
    actualizar_pedidos(
        pedidos_ruta.keys(),
        pedidos
    )

    # ======================================================
    # ACTUALIZAR CLIENTES
    # ======================================================
    actualizar_clientes(
        pedidos_ruta.keys(),
        pedidos,
        clientes
    )

    # ======================================================
    # ACTUALIZAR VEHÍCULO
    # ======================================================
    actualizar_vehiculo(
        vehiculo
    )

    # ======================================================
    # PERSISTIR
    # ======================================================
    id_ruta = persistir_ruta(
        despacho,
        vehiculo,
        list(pedidos_ruta.keys()),
        distancia_total,
        peso_total,
        volumen_total
    )

    # ======================================================
    # MAPA
    # ======================================================
    visualizar_ruta_mapa(

        ruta_optima=ruta_optima,

        pedidos=pedidos_ruta,

        clientes=clientes,

        despacho=despacho,

        nombre_fichero="ruta.html"
    )

    print(
        "\n✔ Ruta generada correctamente"
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