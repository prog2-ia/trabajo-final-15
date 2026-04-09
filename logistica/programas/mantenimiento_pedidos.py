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
# FILTROS
# ==========================================================
def filtrar_pedidos(clientes, pedidos):

    print("\n--- FILTRAR PEDIDOS ---")
    print("1. Por estado")
    print("2. Por cliente origen")
    print("3. Por cliente destino")
    print("4. Por población origen")
    print("5. Por población destino")
    print("0. Todos")

    op = input("Opción: ").strip()

    filtrados = {}

    if op == "1":
        estado = input("Estado: ").lower()
        for pid, p in pedidos.items():
            if p.get("estado", "").lower() == estado:
                filtrados[pid] = p

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

    elif op == "4":
        criterio = normalizar(input("Población origen: "))
        for pid, p in pedidos.items():
            c = clientes.get(p["origen"])
            if c and criterio in normalizar(c.poblacion):
                filtrados[pid] = p

    elif op == "5":
        criterio = normalizar(input("Población destino: "))
        for pid, p in pedidos.items():
            c = clientes.get(p["destino"])
            if c and criterio in normalizar(c.poblacion):
                filtrados[pid] = p

    else:
        filtrados = pedidos

    return filtrados


# ==========================================================
# MOSTRAR PEDIDOS (UNA LÍNEA FORMATEADA)
# ==========================================================
def mostrar_pedidos_formateados(pedidos, clientes):

    print(
        f"{'ID':<8}"
        f"{'ORIGEN':<40}"
        f"{'DESTINO':<40}"
        f"{'PESO':>7}"
        f"{'VOL':>7}"
        f"{'ESTADO':>12}"
    )
    print("-" * 115)

    for pid, p in pedidos.items():

        o = clientes.get(p["origen"])
        d = clientes.get(p["destino"])

        # ORIGEN
        if o:
            nombre_o = f"{o.nombre} {o.apellidos}"[:20]
            direccion_o = (o.direccion[:15] + "...") if len(o.direccion) > 15 else o.direccion
            pob_o = o.poblacion or "N/A"
            o_txt = f"{nombre_o} | {direccion_o} | {pob_o}"
        else:
            o_txt = "N/A"

        # DESTINO
        if d:
            nombre_d = f"{d.nombre} {d.apellidos}"[:20]
            direccion_d = (d.direccion[:15] + "...") if len(d.direccion) > 15 else d.direccion
            pob_d = d.poblacion or "N/A"
            d_txt = f"{nombre_d} | {direccion_d} | {pob_d}"
        else:
            d_txt = "N/A"

        o_txt = o_txt[:39]
        d_txt = d_txt[:39]

        peso = f"{p['peso']:.2f}" if p.get("peso") else "N/A"
        volumen = f"{p['volumen']:.2f}" if p.get("volumen") else "N/A"
        estado = p.get("estado", "N/A")[:12]

        print(
            f"{pid:<8}"
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

    pedidos_filtrados = filtrar_pedidos(clientes, pedidos)

    if not pedidos_filtrados:
        print("❌ No hay pedidos")
        return

    mapa = folium.Map(location=[39.5, -3.5], zoom_start=6)

    for p in pedidos_filtrados.values():

        o = clientes.get(p["origen"])
        d = clientes.get(p["destino"])

        if not o or not d:
            continue

        if not o.coordenadas or not d.coordenadas:
            continue

        folium.PolyLine(
            locations=[o.coordenadas, d.coordenadas],
            color="blue"
        ).add_to(mapa)
        folium.Marker(
            location=o.coordenadas,
            tooltip=f"{o.nombre} {o.apellidos}",
            icon=folium.Icon(color="green")
        ).add_to(mapa)

        folium.Marker(
            location=d.coordenadas,
            tooltip=f"{d.nombre} {d.apellidos}",
            icon=folium.Icon(color="red")
        ).add_to(mapa)

        # folium.Marker(o.coordenadas, icon=folium.Icon(color="green")).add_to(mapa)
        # folium.Marker(d.coordenadas, icon=folium.Icon(color="red")).add_to(mapa)



    # ------------------------------------------------------
    # RUTA CORRECTA UNIFICADA
    # ------------------------------------------------------
    base_dir = encontrar_raiz()  # 👉 devuelve /logistica

    ruta = os.path.join(base_dir, "datos", "mapa_pedidos.html")

    # 🔥 crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # guardar mapa
    mapa.save(ruta)

    print(f"✔ Mapa guardado en: {ruta}")

    # abrir navegador
    webbrowser.open(f"file://{ruta}")
    """
    ruta = Path("../datos/mapa_pedidos.html").resolve()
    mapa.save(ruta)

    print("✔ Mapa generado")
    webbrowser.open(ruta.as_uri())
    """


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

    if not pedidos_filtrados:
        print("❌ Sin resultados")
        return

    mostrar_pedidos_formateados(pedidos_filtrados, clientes)


# ==========================================================
# ALTA / BAJA / MODIFICACIÓN (SIN CAMBIOS IMPORTANTES)
# ==========================================================
def alta_pedido():
    print("\n--- ALTA PEDIDO ---")
    print("👉 Usa el generador automático (test_16)")


def baja_pedido():
    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    encontrados = filtrar_pedidos(clientes, pedidos)

    mostrar_pedidos_formateados(encontrados, clientes)

    pid = input("ID a eliminar: ")

    if pid in pedidos:
        del pedidos[pid]
        guardar_pedidos(pedidos)
        print("✔ Eliminado")


def modificar_pedido():
    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    encontrados = filtrar_pedidos(clientes, pedidos)

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
# MENU
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