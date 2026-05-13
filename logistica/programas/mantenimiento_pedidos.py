# mantenimiento_pedidos.py


# ==========================================================
# MANTENIMIENTO DE PEDIDOS (VERSIÓN PRO FINAL)
# ==========================================================

import os
import sys
import unicodedata
import folium
import webbrowser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.pedido import Pedido
from persistencia.persistencia_clientes import cargar_clientes
from persistencia.persistencia_pedidos import cargar_pedidos, guardar_pedidos
from utiles.utils import encontrar_raiz


# ==========================================================
# NORMALIZACIÓN (SIN TILDES)
# ==========================================================
def normalizar(texto):
    if not texto:
        return ""

    texto = texto.lower()

    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )


# ==========================================================
# FILTRADO DE PEDIDOS
# ==========================================================
def filtrar_pedidos(clientes, pedidos):

    print("\n--- FILTRAR PEDIDOS ---")
    print("1. Por estado")
    print("2. Por cliente origen")
    print("3. Por cliente destino")
    print("4. Por población origen")
    print("5. Por población destino")
    print("6. Todos")
    print("0. Salir")

    op = input("Opción: ").strip()

    filtrados = {}

    # ======================================================
    # SALIR
    # ======================================================
    if op == "0":
        return None

    # ======================================================
    # FILTRAR POR ESTADO
    # ======================================================
    elif op == "1":

        print("\nEstados disponibles:")
        print("1. generado")
        print("2. en_recogida")
        print("3. en_transporte")
        print("4. en_reparto")
        print("5. entregado")

        estados = {
            "1": "generado",
            "2": "en_recogida",
            "3": "en_transporte",
            "4": "en_reparto",
            "5": "entregado"
        }

        opcion_estado = input(
            "\nEstado: "
        ).strip()

        if opcion_estado not in estados:
            print("❌ Estado inválido")
            return None

        estado = estados[opcion_estado]

        for pid, p in pedidos.items():

            if p.get("estado", "").lower() == estado:
                filtrados[pid] = p
    # ======================================================
    # FILTRAR POR CLIENTE ORIGEN
    # ======================================================
    elif op == "2":

        criterio = normalizar(input("Nombre/DNI origen: "))

        for pid, p in pedidos.items():

            c = clientes.get(p["origen"])

            if c and (
                criterio in normalizar(c.nombre)
                or criterio in normalizar(c.apellidos)
                or criterio == normalizar(c.dni)
            ):
                filtrados[pid] = p

    # ======================================================
    # FILTRAR POR CLIENTE DESTINO
    # ======================================================
    elif op == "3":

        criterio = normalizar(input("Nombre/DNI destino: "))

        for pid, p in pedidos.items():

            c = clientes.get(p["destino"])

            if c and (
                criterio in normalizar(c.nombre)
                or criterio in normalizar(c.apellidos)
                or criterio == normalizar(c.dni)
            ):
                filtrados[pid] = p

    # ======================================================
    # FILTRAR POR POBLACIÓN ORIGEN
    # ======================================================
    elif op == "4":

        criterio = normalizar(input("Población origen: "))

        for pid, p in pedidos.items():

            c = clientes.get(p["origen"])

            if c and criterio in normalizar(c.poblacion):
                filtrados[pid] = p

    # ======================================================
    # FILTRAR POR POBLACIÓN DESTINO
    # ======================================================
    elif op == "5":

        criterio = normalizar(input("Población destino: "))

        for pid, p in pedidos.items():

            c = clientes.get(p["destino"])

            if c and criterio in normalizar(c.poblacion):
                filtrados[pid] = p

    # ======================================================
    # TODOS
    # ======================================================
    elif op == "6":

        filtrados = pedidos

    # ======================================================
    # OPCIÓN INVÁLIDA
    # ======================================================
    else:

        print("❌ Opción inválida")
        return None

    return filtrados


# ==========================================================
# MOSTRAR PEDIDOS FORMATEADOS
# ==========================================================
def mostrar_pedidos_formateados(pedidos, clientes):
    print(
        f"{'ID':<8}"
        f"{'DELEGACIÓN':<25}"
        f"{'ORIGEN':<40}"
        f"{'DESTINO':<40}"
        f"{'PESO':>7}"
        f"{'VOL':>7}"
        f"{'ESTADO':>12}"
    )

    print("-" * 145)

    # ======================================================
    # ORDENAR POR DELEGACIÓN
    # ======================================================
    # ======================================================
    # ORDENAR POR POBLACIÓN Y DELEGACIÓN
    # ======================================================
    pedidos_ordenados = sorted(

        pedidos.items(),

        key=lambda item: (

            # --------------------------------------------------
            # POBLACIÓN
            # --------------------------------------------------
            (
                    (
                            item[1]
                            and
                            clientes.get(item[1]["origen"])
                            and
                            clientes[item[1]["origen"]].delegacion_cercana
                            and
                            hasattr(
                                clientes[item[1]["origen"]].delegacion_cercana,
                                "poblacion"
                            )
                    )

                    and

                    str(
                        clientes[
                            item[1]["origen"]
                        ].delegacion_cercana.poblacion
                    ).lower()

                    or ""
            ),

            # --------------------------------------------------
            # DELEGACIÓN
            # --------------------------------------------------
            (
                    (
                            item[1]
                            and
                            clientes.get(item[1]["origen"])
                            and
                            clientes[item[1]["origen"]].delegacion_cercana
                    )

                    and

                    clientes[
                        item[1]["origen"]
                    ].delegacion_cercana.nombre.lower()

                    or ""
            )
        )
    )
    for pid, p in pedidos_ordenados:

        o = clientes.get(p["origen"])
        d = clientes.get(p["destino"])

        # ======================================================
        # ORIGEN
        # ======================================================
        if o:

            nombre_o = f"{o.nombre} {o.apellidos}"[:20]
            direccion_o = (
                (o.direccion[:15] + "...")
                if len(o.direccion) > 15
                else o.direccion
            )

            pob_o = o.poblacion or "N/A"
            o_txt = f"{nombre_o} | {direccion_o} | {pob_o}"

        else:
            o_txt = "N/A"

        # ======================================================
        # DESTINO
        # ======================================================
        if d:

            nombre_d = f"{d.nombre} {d.apellidos}"[:20]
            direccion_d = (
                (d.direccion[:15] + "...")
                if len(d.direccion) > 15
                else d.direccion
            )

            pob_d = d.poblacion or "N/A"
            d_txt = f"{nombre_d} | {direccion_d} | {pob_d}"

        else:
            d_txt = "N/A"

        o_txt = o_txt[:39]
        d_txt = d_txt[:39]

        # ======================================================
        # DELEGACIÓN
        # ======================================================
        delegacion = "N/A"

        if o and o.delegacion_cercana:
            nombre_delegacion = (
                o.delegacion_cercana.nombre
            )

            poblacion_delegacion = (
                o.delegacion_cercana.poblacion
                if hasattr(
                    o.delegacion_cercana,
                    "poblacion"
                )
                else "N/A"
            )

            delegacion = (
                f"{nombre_delegacion} | "
                f"{poblacion_delegacion}"
            )[:24]

        peso = f"{p['peso']:.2f}" if p.get("peso") else "N/A"
        volumen = f"{p['volumen']:.2f}" if p.get("volumen") else "N/A"
        estado = p.get("estado", "N/A")[:12]

        print(
            f"{pid:<8}"
            f"{delegacion:<25}"
            f"{o_txt:<40}"
            f"{d_txt:<40}"
            f"{peso:>7}"
            f"{volumen:>7}"
            f"{estado:>12}"
        )


# ==========================================================
# MAPA DE PEDIDOS
# ==========================================================
def ver_mapa_pedidos():

    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    # pedidos_filtrados = filtrar_pedidos(clientes, pedidos)
    pedidos_filtrados = pedidos

    # ======================================================
    # SI PULSA 0 -> SALIR
    # ======================================================
    if pedidos_filtrados is None:
        return

    if not pedidos_filtrados:
        print("❌ No hay pedidos")
        return

    # ======================================================
    # CREAR MAPA
    # ======================================================
    mapa = folium.Map(location=[39.5, -3.5], zoom_start=6)

    for p in pedidos_filtrados.values():

        o = clientes.get(p["origen"])
        d = clientes.get(p["destino"])

        if not o or not d:
            continue

        if not o.coordenadas or not d.coordenadas:
            continue

        # ======================================================
        # LÍNEA ENTRE ORIGEN Y DESTINO
        # ======================================================
        folium.PolyLine(
            locations=[o.coordenadas, d.coordenadas],
            color="blue"
        ).add_to(mapa)

        # ======================================================
        # MARCADOR ORIGEN
        # ======================================================
        folium.Marker(
            location=o.coordenadas,
            tooltip=f"{o.nombre} {o.apellidos}",
            icon=folium.Icon(color="green")
        ).add_to(mapa)

        # ======================================================
        # MARCADOR DESTINO
        # ======================================================
        folium.Marker(
            location=d.coordenadas,
            tooltip=f"{d.nombre} {d.apellidos}",
            icon=folium.Icon(color="red")
        ).add_to(mapa)

    # ======================================================
    # RUTA DEL MAPA
    # ======================================================
    base_dir = encontrar_raiz()

    ruta = os.path.join(base_dir, "datos", "mapa_pedidos.html")

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # ======================================================
    # GUARDAR MAPA
    # ======================================================
    mapa.save(ruta)

    print(f"✔ Mapa guardado en: {ruta}")

    # ======================================================
    # ABRIR NAVEGADOR
    # ======================================================
    webbrowser.open(f"file://{ruta}")


# ==========================================================
# LISTAR PEDIDOS
# ==========================================================
def listar_pedidos():

    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    if not pedidos:
        print("❌ No hay pedidos")
        return

    pedidos_filtrados = filtrar_pedidos(clientes, pedidos)

    # ======================================================
    # SI PULSA 0 -> SALIR
    # ======================================================
    if pedidos_filtrados is None:
        return

    if not pedidos_filtrados:
        print("❌ Sin resultados")
        return

    mostrar_pedidos_formateados(pedidos_filtrados, clientes)


# ==========================================================
# ALTA PEDIDO
# ==========================================================
def alta_pedido():

    print("\n--- ALTA PEDIDO ---")
    print("👉 Usa el generador automático (test_16)")


# ==========================================================
# BAJA PEDIDO
# ==========================================================
def baja_pedido():

    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    encontrados = filtrar_pedidos(clientes, pedidos)

    # ======================================================
    # SI PULSA 0 -> SALIR
    # ======================================================
    if encontrados is None:
        return

    if not encontrados:
        print("❌ Sin resultados")
        return

    mostrar_pedidos_formateados(encontrados, clientes)

    pid = input("ID a eliminar: ")

    if pid in pedidos:

        del pedidos[pid]

        guardar_pedidos(pedidos)

        print("✔ Eliminado")


# ==========================================================
# MODIFICAR PEDIDO
# ==========================================================
def modificar_pedido():

    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    encontrados = filtrar_pedidos(clientes, pedidos)

    # ======================================================
    # SI PULSA 0 -> SALIR
    # ======================================================
    if encontrados is None:
        return

    if not encontrados:
        print("❌ Sin resultados")
        return

    mostrar_pedidos_formateados(encontrados, clientes)

    pid = input("ID a modificar: ")

    if pid not in pedidos:
        return

    p = pedidos[pid]

    p["peso"] = float(input(f"Peso [{p['peso']}]: ") or p["peso"])

    p["volumen"] = float(input(f"Volumen [{p['volumen']}]: ") or p["volumen"])

    guardar_pedidos(pedidos)

    print("✔ Modificado")


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def ejecutar():

    while True:

        print("\n=== MANTENIMIENTO PEDIDOS ===")
        print("1 Alta")
        print("2 Baja")
        print("3 Modificar")
        print("4 Listar")
        print("5 Ver mapa pedidos")
        print("0 Salir")

        op = input("Opción: ")

        if op == "1":
            alta_pedido()

        elif op == "2":
            baja_pedido()

        elif op == "3":
            modificar_pedido()

        elif op == "4":
            listar_pedidos()

        elif op == "5":
            ver_mapa_pedidos()

        elif op == "0":
            break


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()

