"""
==========================================================
PROGRAMA: GESTIÓN DE CLIENTES (VERSIÓN FINAL CORREGIDA PRO)
==========================================================

✔ Dirección = STRING
✔ Coordenadas geográficas
✔ Población y provincia
✔ Delegación cercana automática
✔ Distancia al despacho

✔ Compatible con nueva persistencia (sobrescribir=True)
✔ Sin problemas de memoria (recarga dinámica)
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
import utiles.utils as utils
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.utils import distancia_km
from utiles.geolocalizacion import geocodificar


# ==========================================================
# DATOS BASE
# ==========================================================
nombres = [
    "Juan", "Maria", "Luis", "Ana", "Pedro", "Lucia",
    "Carlos", "Elena", "Miguel", "Carmen"
]

apellidos = [
    "Garcia", "Perez", "Lopez", "Sanchez", "Martinez",
    "Gomez", "Fernandez", "Ruiz", "Diaz", "Moreno"
]

direcciones_validas = [
    "Avenida Maisonnave 1, Alicante, España",
    "Avenida Libertad 20, Elche, España",
    "Avenida Mediterraneo 30, Benidorm, España",
    "Gran Via 1, Madrid, España",
    "Calle Alcala 50, Madrid, España"
]


# ==========================================================
# FUNCIONES AUXILIARES
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
        print(f"📍 Coincide con despacho: {mejor.nombre}")
        print("❌ Cliente NO guardado\n")
        return False

    cliente._delegacion_cercana = mejor
    cliente._distancia_despacho = round(min_dist, 2)

    return True


# ==========================================================
# ALTA CLIENTE
# ==========================================================
def alta_cliente_interactiva():

    global clientes
    clientes = cargar_clientes()

    print("\n--- ALTA CLIENTE PRO ---")

    # DNI
    while True:

        dni_input = input("DNI (ENTER = automático): ").strip().upper()

        if not dni_input:

            while True:
                dni = utils.generar_dni_real()
                if dni not in clientes:
                    print(f"👉 DNI generado: {dni}")
                    break

            break

        if not utils.validar_dni_real(dni_input):
            print("❌ DNI inválido")
            continue

        if dni_input in clientes:
            print("❌ El cliente ya existe")
            continue

        dni = dni_input
        break

    # DATOS
    nombre = input("Nombre: ").strip()
    apellido1 = input("Primer apellido: ").strip()
    apellido2 = input("Segundo apellido: ").strip()

    # DIRECCIÓN
    while True:

        direccion = input("\nDirección: ").strip()

        coord = geocodificar(direccion)

        if coord:
            print("✔ Dirección válida")
            break
        else:
            print("❌ Dirección no válida")

    c = Cliente(dni, nombre, f"{apellido1} {apellido2}", direccion)

    if not calcular_datos_logisticos(c):
        print("❌ Cliente NO guardado")
        return

    clientes[dni] = c
    guardar_clientes({dni: c})

    clientes = cargar_clientes()

    print("\n✔ Cliente añadido correctamente")
    print(f"📍 Delegación: {c.delegacion_cercana.nombre if c.delegacion_cercana else 'N/A'}")
    print(f"📏 Distancia: {c.distancia_despacho} km")
    print(f"🌍 Población: {c.poblacion}")
    print(f"🗺️ Provincia: {c.provincia}")


# ==========================================================
# BAJA
# ==========================================================
def baja_cliente_interactiva():

    global clientes
    clientes = cargar_clientes()

    print("\n--- BAJA CLIENTE ---")

    dni = input("DNI: ").strip()

    if dni not in clientes:
        print("❌ No encontrado")
        return

    del clientes[dni]

    # 🔥 CLAVE
    guardar_clientes(clientes, sobrescribir=True)

    clientes = cargar_clientes()

    print("✔ Eliminado")


# ==========================================================
# MODIFICAR
# ==========================================================
def modificar_cliente_interactiva():

    global clientes
    clientes = cargar_clientes()

    print("\n--- MODIFICAR CLIENTE ---")

    dni = input("DNI: ").strip()

    if dni not in clientes:
        print("❌ No encontrado")
        return

    c_original = clientes[dni]

    nuevo_nombre = input(f"\nNombre [{c_original.nombre}]: ").strip() or c_original.nombre
    nuevos_apellidos = input(f"Apellidos [{c_original.apellidos}]: ").strip() or c_original.apellidos
    nueva_direccion = input(f"Dirección [{c_original.direccion}]: ").strip() or c_original.direccion

    coord = geocodificar(nueva_direccion)

    if not coord:
        print("❌ Dirección no válida")
        return

    c_temp = Cliente(dni, nuevo_nombre, nuevos_apellidos, nueva_direccion)
    c_temp._coordenadas = coord

    try:
        c_temp.actualizar_datos_geo()
    except:
        pass

    c_temp._poblacion = input(f"Población [{c_temp.poblacion}]: ").strip() or c_temp.poblacion
    c_temp._provincia = input(f"Provincia [{c_temp.provincia}]: ").strip() or c_temp.provincia

    if not calcular_datos_logisticos(c_temp):
        return

    clientes[dni] = c_temp
    guardar_clientes({dni: c_temp})

    clientes = cargar_clientes()

    print("✔ Cliente modificado correctamente")


# ==========================================================
# LISTAR
# ==========================================================
def listar_clientes():

    global clientes
    clientes = cargar_clientes()

    print("\n--- LISTADO CLIENTES ---")

    if not clientes:
        print("No hay clientes")
        return

    for c in clientes.values():
        print(f"{c.dni} | {c.nombre} {c.apellidos} | {c.poblacion} | {c.provincia}")


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