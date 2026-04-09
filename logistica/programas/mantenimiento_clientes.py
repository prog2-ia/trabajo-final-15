"""
==========================================================
PROGRAMA: GESTIÓN DE CLIENTES (VERSIÓN FINAL PRO DEFINITIVA)
==========================================================
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
import utiles.utils as utils
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from persistencia.persistencia_pedidos import cargar_pedidos
from utiles.utils import distancia_km
from utiles.geolocalizacion import geocodificar


# ==========================================================
# NORMALIZADOR
# ==========================================================
def normalizar(txt):
    return (txt or "").strip().lower()


# ==========================================================
# 🔥 SELECCIÓN DE CLIENTE (REUTILIZABLE)
# ==========================================================
def seleccionar_cliente(clientes):

    entrada = input("\nDNI o nombre/apellidos: ").strip()
    entrada_norm = normalizar(entrada)

    encontrados = {}

    for c in clientes.values():
        nombre = f"{c.nombre} {c.apellidos}"

        if entrada.upper() == c.dni or entrada_norm in normalizar(nombre):
            encontrados[c.dni] = c

    if not encontrados:
        print("❌ No encontrado")
        return None

    if len(encontrados) == 1:
        return list(encontrados.values())[0]

    # múltiples → elegir
    lista = list(encontrados.values())

    print("\nCoincidencias:")
    for i, c in enumerate(lista, 1):
        print(f"{i}. {c.dni} | {c.nombre} {c.apellidos}")

    try:
        idx = int(input("Selecciona: ")) - 1
        return lista[idx]
    except:
        print("❌ Selección inválida")
        return None


# ==========================================================
# FUNCION LOGÍSTICA
# ==========================================================
def calcular_datos_logisticos(cliente):

    delegaciones = cargar_delegaciones()

    coord = geocodificar(cliente.direccion)

    if not coord:
        print("❌ No se pudo geolocalizar la dirección")
        return False

    cliente._coordenadas = coord

    if not cliente._poblacion or not cliente._provincia:
        cliente.actualizar_datos_geo()

    mejor = None
    min_dist = float("inf")

    for d in delegaciones:

        if not d.coordenadas:
            continue

        dist = distancia_km(coord, d.coordenadas)

        if dist < min_dist:
            min_dist = dist
            mejor = d

    if not mejor:
        print("❌ No se encontró delegación cercana")
        return False

    if min_dist < 0.1:
        print("\n⚠️ Dirección sospechosa")
        return False

    cliente._delegacion_cercana = mejor
    cliente._distancia_despacho = round(min_dist, 2)

    return True


# ==========================================================
# ALTA CLIENTE
# ==========================================================
def alta_cliente_interactiva():

    clientes = cargar_clientes()

    print("\n--- ALTA CLIENTE ---")

    while True:
        dni = input("DNI (ENTER auto): ").strip().upper()

        if not dni:
            dni = utils.generar_dni_real()

        if not utils.validar_dni_real(dni):
            print("❌ DNI inválido")
            continue

        if dni in clientes:
            print("❌ Ya existe")
            continue

        break

    nombre = input("Nombre: ").strip()
    apellidos = input("Apellidos: ").strip()

    while True:
        direccion = input("Dirección: ").strip()
        if geocodificar(direccion):
            break
        print("❌ Dirección inválida")

    c = Cliente(dni, nombre, apellidos, direccion)

    if not calcular_datos_logisticos(c):
        return

    clientes[dni] = c
    guardar_clientes({dni: c})

    print("✔ Cliente creado")


# ==========================================================
# BAJA
# ==========================================================
def baja_cliente_interactiva():

    clientes = cargar_clientes()

    print("\n--- BAJA CLIENTE ---")

    c = seleccionar_cliente(clientes)
    if not c:
        return

    confirm = input(f"¿Eliminar {c.nombre} {c.apellidos}? (s/n): ").lower()

    if confirm != "s":
        print("❌ Cancelado")
        return

    del clientes[c.dni]
    guardar_clientes(clientes, sobrescribir=True)

    print("✔ Eliminado")


# ==========================================================
# MODIFICAR
# ==========================================================
def modificar_cliente_interactiva():

    clientes = cargar_clientes()

    print("\n--- MODIFICAR CLIENTE ---")

    c = seleccionar_cliente(clientes)
    if not c:
        return

    nombre = input(f"Nombre [{c.nombre}]: ") or c.nombre
    apellidos = input(f"Apellidos [{c.apellidos}]: ") or c.apellidos
    direccion = input(f"Dirección [{c.direccion}]: ") or c.direccion

    if not geocodificar(direccion):
        print("❌ Dirección inválida")
        return

    nuevo = Cliente(c.dni, nombre, apellidos, direccion)

    if not calcular_datos_logisticos(nuevo):
        return

    clientes[c.dni] = nuevo
    guardar_clientes({c.dni: nuevo})

    print("✔ Modificado")


# ==========================================================
# LISTAR CLIENTES (PRO)
# ==========================================================
def listar_clientes():

    clientes = cargar_clientes()
    pedidos = cargar_pedidos()

    if not clientes:
        print("No hay clientes")
        return

    entrada = input("\nDNI, nombre/apellidos o T (todos): ").strip()
    entrada_norm = normalizar(entrada)

    if entrada_norm == "t":
        clientes_filtrados = clientes
        modo_todos = True
    else:
        clientes_filtrados = {}

        for c in clientes.values():
            nombre = f"{c.nombre} {c.apellidos}"

            if entrada.upper() == c.dni or entrada_norm in normalizar(nombre):
                clientes_filtrados[c.dni] = c

        if not clientes_filtrados:
            print("❌ No encontrado")
            return

        if len(clientes_filtrados) > 1:
            lista = list(clientes_filtrados.values())

            for i, c in enumerate(lista, 1):
                print(f"{i}. {c.dni} | {c.nombre} {c.apellidos}")

            idx = int(input("Selecciona: ")) - 1
            clientes_filtrados = {lista[idx].dni: lista[idx]}

        modo_todos = False

    estado_filtro = None

    if modo_todos:

        print("\n1 generado 2 recogida 3 transporte 4 reparto 5 entregado T todos")

        mapa = {
            "1": "generado",
            "2": "en_recogida",
            "3": "en_transporte",
            "4": "en_reparto",
            "5": "entregado"
        }

        op = input("Estado: ").strip().lower()

        if op != "t":
            estado_filtro = mapa.get(op)

    print(
        f"{'DNI':<12}{'NOMBRE':<25}{'POBLACIÓN':<18}"
        f"{'PED':<6}{'ORIGEN':<18}{'DESTINO':<18}{'ESTADO':<12}"
    )
    print("-" * 110)

    for c in clientes_filtrados.values():

        lista_ids = getattr(c, "_pedidos_en_curso", []) + getattr(c, "_pedidos_terminados", [])

        for pid in lista_ids:

            p = pedidos.get(pid)
            if not p:
                continue

            estado = p["estado"]

            if estado_filtro and estado != estado_filtro:
                continue

            o = clientes.get(p["origen"])
            d = clientes.get(p["destino"])

            print(
                f"{c.dni:<12}"
                f"{(c.nombre + ' ' + c.apellidos)[:24]:<25}"
                f"{(c.poblacion or 'N/A')[:17]:<18}"
                f"{pid:<6}"
                f"{(o.poblacion if o else 'N/A'):<18}"
                f"{(d.poblacion if d else 'N/A'):<18}"
                f"{estado:<12}"
            )


# ==========================================================
# MENU
# ==========================================================
def ejecutar():

    while True:

        print("\nGESTION CLIENTES")
        print("1 Alta")
        print("2 Baja")
        print("3 Modificar")
        print("4 Listar")
        print("0 Salir")

        op = input("Opción: ")

        if op == "1":
            alta_cliente_interactiva()
        elif op == "2":
            baja_cliente_interactiva()
        elif op == "3":
            modificar_cliente_interactiva()
        elif op == "4":
            listar_clientes()
        elif op == "0":
            break


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()