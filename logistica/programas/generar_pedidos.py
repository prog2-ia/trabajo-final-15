# ==========================================================
# GENERADOR DE PEDIDOS (VERSIÓN FINAL PRO CON MENÚ)
# ==========================================================

import sys
import os
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.pedido import Pedido
from persistencia.persistencia_clientes import cargar_clientes, guardar_clientes
from persistencia.persistencia_pedidos import (
    cargar_pedidos,
    guardar_pedidos,
    añadir_pedidos,
    borrar_pedidos,
    obtener_ruta_pedidos
)

# ==========================================================
# ACTUALIZAR CLIENTES CON PEDIDOS
# ==========================================================
def actualizar_clientes_con_pedidos():
    """
    Actualiza en clientes:
    - pedidos_en_curso
    - pedidos_terminados
    según el estado del pedido
    """

    print("\n🔄 ACTUALIZANDO CLIENTES CON PEDIDOS...")

    pedidos = cargar_pedidos()
    clientes = cargar_clientes()

    if not pedidos:
        print("❌ No hay pedidos")
        return

    if not clientes:
        print("❌ No hay clientes")
        return

    # ------------------------------------------------------
    # LIMPIAR LISTAS
    # ------------------------------------------------------
    for c in clientes.values():
        c._pedidos_en_curso = []
        c._pedidos_terminados = []

    # ------------------------------------------------------
    # CLASIFICACIÓN
    # ------------------------------------------------------
    estados_activos = {
        "generado",
        "en_recogida",
        "en_transporte",
        "en_reparto"
    }

    for pid, p in pedidos.items():

        origen = clientes.get(p["origen"])
        destino = clientes.get(p["destino"])

        estado = p.get("estado", "").lower()

        # -------------------------
        # PEDIDOS EN CURSO
        # -------------------------
        if estado in estados_activos:

            if origen:
                origen._pedidos_en_curso.append(pid)

            if destino:
                destino._pedidos_en_curso.append(pid)

        # -------------------------
        # PEDIDOS TERMINADOS
        # -------------------------
        elif estado == "entregado":

            if origen:
                origen._pedidos_terminados.append(pid)

            if destino:
                destino._pedidos_terminados.append(pid)

    # ------------------------------------------------------
    # GUARDAR
    # ------------------------------------------------------
    guardar_clientes(clientes)

    print("✔ Clientes actualizados correctamente")

# ==========================================================
# PESO (90% < 2kg)
# ==========================================================
def generar_peso():
    if random.random() < 0.9:
        return round(random.uniform(0.1, 2), 2)
    return round(random.uniform(2, 100), 2)


# ==========================================================
# VOLUMEN (COHERENTE)
# ==========================================================
def generar_volumen(peso):
    densidad = random.uniform(0.05, 0.3)
    volumen = peso / densidad
    return round(min(volumen, 1000), 2)


# ==========================================================
# SERVICIO
# ==========================================================
def generar_servicio():
    return "express" if random.random() < 0.3 else "standard"


# ==========================================================
# EXTRAER POBLACIÓN
# ==========================================================
def extraer_poblacion(cliente):
    """
    Devuelve la población de un cliente usando primero el atributo
    persistido y, si no existe, intenta obtenerla desde la dirección.
    """
    if hasattr(cliente, "poblacion") and cliente.poblacion and cliente.poblacion != "N/A":
        return cliente.poblacion

    try:
        partes = cliente.direccion.split(",")
        return partes[-3].strip()
    except Exception:
        return "N/A"


# ==========================================================
# BORRAR TODOS LOS PEDIDOS
# ==========================================================
def eliminar_todos_los_pedidos():
    """
    Borra el fichero completo de pedidos.
    """
    print("\n===== BORRAR PEDIDOS =====")

    confirm = input("⚠️ ¿Borrar TODOS los pedidos? (s/n): ").strip().lower()

    if confirm != "s":
        print("❌ Operación cancelada")
        return

    if borrar_pedidos():
        print("🗑️ Fichero de pedidos eliminado correctamente")
    else:
        print("⚠️ No existe fichero de pedidos")


# ==========================================================
# GENERAR PEDIDOS
# ==========================================================
def generar_pedidos():

    print("\n===== GENERADOR DE PEDIDOS =====")

    clientes_dict = cargar_clientes()

    if not clientes_dict:
        print("❌ ERROR: No hay clientes")
        print("👉 Debes generar clientes primero")
        return

    clientes = list(clientes_dict.values())

    if len(clientes) < 2:
        print("❌ ERROR: Se necesitan al menos 2 clientes")
        return

    # ------------------------------------------------------
    # INPUT
    # ------------------------------------------------------
    try:
        n = int(input("Número de pedidos a generar: "))
    except Exception:
        print("❌ Número inválido")
        return

    if n <= 0:
        print("❌ El número debe ser mayor que cero")
        return

    # ------------------------------------------------------
    # GENERACIÓN
    # ------------------------------------------------------
    generados = 0
    pedidos_generados = []
    nuevos = {}

    for _ in range(n):

        origen, destino = random.sample(clientes, 2)

        peso = generar_peso()
        volumen = generar_volumen(peso)
        servicio = generar_servicio()

        try:
            p = Pedido(
                origen=origen,
                destino=destino,
                peso=peso,
                volumen=volumen,
                nivel_servicio=servicio
            )

            pedidos_generados.append(p)

            nuevos[p.id] = {
                "origen": origen.dni,
                "destino": destino.dni,
                "peso": peso,
                "volumen": volumen,
                "km": p.km,
                "estado": p.estado_pedido,
                "fecha_pedido": str(p.fecha_pedido),
                "fecha_entrega": None
            }

            generados += 1

        except Exception as e:
            print(f"⚠️ Error creando pedido: {e}")
            continue

    # ------------------------------------------------------
    # GUARDAR
    # ------------------------------------------------------
    if nuevos:
        añadir_pedidos(nuevos)

    print(f"\n✔ Pedidos generados: {generados}")

    # ------------------------------------------------------
    # MOSTRAR PEDIDOS GENERADOS
    # ------------------------------------------------------
    print("\n===== PEDIDOS GENERADOS =====")

    for p in pedidos_generados:

        o = p._origen
        d = p._destino

        origen_txt = f"{o.nombre} {o.apellidos} ({extraer_poblacion(o)})"
        destino_txt = f"{d.nombre} {d.apellidos} ({extraer_poblacion(d)})"

        print(
            f"[{p.id}] "
            f"{origen_txt} → "
            f"{destino_txt} | "
            f"{p._peso:.2f} kg | "
            f"{p._volumen:.2f} L | "
            f"{p.km:.2f} km"
        )

    print(f"\n📁 Guardados en: {obtener_ruta_pedidos()}")


# ==========================================================
# LISTAR PEDIDOS
# ==========================================================
# ==========================================================
# LISTAR PEDIDOS (FORMATO TABLA PRO)
# ==========================================================
def listar_pedidos():
    """
    Lista todos los pedidos persistidos en formato tabla completa.
    """

    print("\n===== LISTADO PEDIDOS =====")

    data = cargar_pedidos()
    clientes = cargar_clientes()

    if not data:
        print("❌ No hay pedidos")
        return

    # ------------------------------------------------------
    # CABECERA
    # ------------------------------------------------------
    print(
        f"{'ID':<8}"
        f"{'ORIGEN':<30}"
        f"{'DESTINO':<30}"
        f"{'PESO':>8}"
        f"{'VOL':>8}"
        f"{'KM':>8}"
        f"{'ESTADO':>12}"
    )
    print("-" * 110)

    # ------------------------------------------------------
    # FILAS
    # ------------------------------------------------------
    for pid, p in data.items():

        origen = clientes.get(p["origen"])
        destino = clientes.get(p["destino"])

        # -------------------------
        # ORIGEN
        # -------------------------
        if origen:
            nombre_o = f"{origen.nombre} {origen.apellidos}"
            pob_o = extraer_poblacion(origen)
            o_txt = f"{nombre_o} ({pob_o})"
        else:
            o_txt = "N/A"

        # -------------------------
        # DESTINO
        # -------------------------
        if destino:
            nombre_d = f"{destino.nombre} {destino.apellidos}"
            pob_d = extraer_poblacion(destino)
            d_txt = f"{nombre_d} ({pob_d})"
        else:
            d_txt = "N/A"

        # recorte para formato
        o_txt = o_txt[:29]
        d_txt = d_txt[:29]

        # -------------------------
        # NUMÉRICOS
        # -------------------------
        peso = f"{p.get('peso', 0):.2f}" if p.get("peso") else "N/A"
        volumen = f"{p.get('volumen', 0):.2f}" if p.get("volumen") else "N/A"
        km = f"{p.get('km', 0):.2f}" if p.get("km") else "N/A"

        estado = p.get("estado", "N/A")[:12]

        # -------------------------
        # PRINT
        # -------------------------
        print(
            f"{pid:<8}"
            f"{o_txt:<30}"
            f"{d_txt:<30}"
            f"{peso:>8}"
            f"{volumen:>8}"
            f"{km:>8}"
            f"{estado:>12}"
        )

    print(f"\nTOTAL PEDIDOS: {len(data)}")

# ==========================================================
# MENÚ
# ==========================================================
def ejecutar():
    """
    Menú principal de gestión rápida de pedidos de prueba.
    """
    while True:
        print("\n=== GESTIÓN DE PEDIDOS DE PRUEBA ===")
        print("1. Borrar todos los pedidos")
        print("2. Generar pedidos")
        print("3. Listar pedidos")
        print("4. Actualizar clientes con pedidos")
        print("0. Salir")

        op = input("Opción: ").strip()

        if op == "1":
            eliminar_todos_los_pedidos()
        elif op == "2":
            generar_pedidos()
        elif op == "3":
            listar_pedidos()
        elif op == "4":
            actualizar_clientes_con_pedidos()
        elif op == "0":
            break
        else:
            print("❌ Opción inválida")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()