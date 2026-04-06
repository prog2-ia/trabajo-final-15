"""
==========================================================
PROGRAMA: GESTIÓN DE CLIENTES (CRUD + GENERACIÓN AUTOMÁTICA)
==========================================================

Adaptado a la nueva arquitectura:

✔ Dirección = STRING
✔ Coordenadas geográficas automáticas
✔ Delegación más cercana automática
✔ Distancia al despacho en km

FUNCIONALIDADES:
- Alta / Baja / Modificación / Listado
- Generación automática de clientes
- Persistencia JSON
"""

# ==========================================================
# IMPORTS
# ==========================================================
import random
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
import utiles.utils as utils
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.utils import distancia_km


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

    coord = utils.geocodificar_direccion(cliente.direccion)

    # ------------------------------------------------------
    # ❌ NO GEOLOCALIZADO → BLOQUEAR
    # ------------------------------------------------------
    if not coord:
        print("❌ No se pudo geolocalizar la dirección")
        return False

    cliente._coordenadas = coord

    mejor = None
    min_dist = float("inf")

    for d in delegaciones:

        if not d.coordenadas:
            continue

        dist = distancia_km(coord, d.coordenadas)

        if dist < min_dist:
            min_dist = dist
            mejor = d

    # ------------------------------------------------------
    # ❌ SIN DELEGACIÓN → BLOQUEAR
    # ------------------------------------------------------
    if not mejor:
        print("❌ No se encontró delegación cercana")
        return False

    # ------------------------------------------------------
    # 🚨 DETECTAR GEOLOCALIZACIÓN SOSPECHOSA
    # ------------------------------------------------------
    if min_dist < 0.1:
        print("\n⚠️ Dirección sospechosa")
        print(f"📍 Coincide con despacho: {mejor.nombre}")
        print("❌ Cliente NO guardado\n")
        return False

    # ------------------------------------------------------
    # ✔ OK → ASIGNAR
    # ------------------------------------------------------
    cliente._delegacion_cercana = mejor
    cliente._provincia = mejor.provincia
    cliente._distancia_despacho = round(min_dist, 2)

    return True
# ==========================================================
# GENERACIÓN AUTOMÁTICA
# ==========================================================
def generar_cliente():

    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)

    while apellido2 == apellido1:
        apellido2 = random.choice(apellidos)

    direccion = random.choice(direcciones_validas)

    c = Cliente(
        dni=utils.generar_dni_real(),
        nombre=random.choice(nombres),
        apellidos=f"{apellido1} {apellido2}",
        direccion=direccion
    )

    if not calcular_datos_logisticos(c):
        return None

    return c


# ==========================================================
# CARGA INICIAL
# ==========================================================
clientes = cargar_clientes()


# ==========================================================
# ALTA CLIENTE
# ==========================================================
def alta_cliente_interactiva():

    print("\n--- ALTA CLIENTE PRO ---")

    # ==========================================================
    # DNI (AUTO GENERADO SI ENTER)
    # ==========================================================
    # ==========================================================
    # DNI (AUTO + VALIDACIÓN REAL)
    # ==========================================================
    while True:

        dni_input = input("DNI (ENTER = automático): ").strip().upper()

        # ------------------------------------------------------
        # CASO 1: ENTER → generar automático
        # ------------------------------------------------------
        if not dni_input:

            while True:
                dni = utils.generar_dni_real()
                if dni not in clientes:
                    print(f"👉 DNI generado: {dni}")
                    break

            break

        # ------------------------------------------------------
        # CASO 2: VALIDACIÓN MANUAL
        # ------------------------------------------------------
        if not utils.validar_dni_real(dni_input):
            print("❌ DNI inválido (ej: 12345678Z)")
            continue

        if dni_input in clientes:
            print("❌ El cliente ya existe")
            continue

        dni = dni_input
        break
    # ==========================================================
    # DATOS PERSONALES
    # ==========================================================
    nombre = input("Nombre: ").strip()
    apellido1 = input("Primer apellido: ").strip()
    apellido2 = input("Segundo apellido: ").strip()

    # ==========================================================
    # DIRECCIÓN (CON SUGERENCIAS + VALIDACIÓN)
    # ==========================================================
    direccion = ""

    while True:

        texto = input("\nDirección: ").strip()


        # ------------------------------------------------------
        # VALIDACIÓN EN TIEMPO REAL
        # ------------------------------------------------------
        coord = utils.geocodificar_direccion(texto)

        if coord:
            print("✔ Dirección válida")
            direccion = texto
            break
        else:
            print("❌ Dirección no válida, intenta de nuevo")

    # ==========================================================
    # CREAR CLIENTE
    # ==========================================================
    c = Cliente(dni, nombre, f"{apellido1} {apellido2}", direccion)

    # ==========================================================
    # CALCULAR DATOS LOGÍSTICOS
    # ==========================================================
    if not calcular_datos_logisticos(c):
        print("❌ Cliente NO actualizado por error de geolocalización")
        return
    # ==========================================================
    # GUARDAR
    # ==========================================================
    clientes[dni] = c
    guardar_clientes({dni: c})

    print("\n✔ Cliente añadido correctamente")
    print(f"📍 Delegación: {c.delegacion_cercana.nombre if c.delegacion_cercana else 'N/A'}")
    print(f"📏 Distancia: {c.distancia_despacho} km")


# ==========================================================
# BAJA CLIENTE
# ==========================================================
def baja_cliente_interactiva():

    print("\n--- BAJA CLIENTE ---")

    if not clientes:
        print("No hay clientes")
        return

    dni = input("DNI a eliminar: ").strip()

    if dni not in clientes:
        print("No encontrado")
        return

    del clientes[dni]
    guardar_clientes(clientes)

    print("✔ Cliente eliminado")


# ==========================================================
# MODIFICAR CLIENTE
# ==========================================================
def modificar_cliente_interactiva():

    print("\n--- MODIFICAR CLIENTE ---")

    dni = input("DNI: ").strip()

    if dni not in clientes:
        print("No encontrado")
        return

    c = clientes[dni]

    nombre = input(f"Nombre [{c.nombre}]: ") or c.nombre
    apellidos = input(f"Apellidos [{c.apellidos}]: ") or c.apellidos
    direccion = input(f"Dirección [{c.direccion}]: ") or c.direccion

    c._nombre = nombre
    c._apellidos = apellidos
    c._direccion = direccion

    if not calcular_datos_logisticos(c):
        print("❌ Dirección no válida")
        return

    guardar_clientes({dni: c})

    print("✔ Cliente modificado")


# ==========================================================
# LISTAR CLIENTES
# ==========================================================
def listar_clientes():

    print("\n--- LISTADO CLIENTES ---")

    if not clientes:
        print("No hay clientes")
        return

    for c in sorted(clientes.values(), key=lambda x: (x.apellidos, x.nombre)):

        print("\n------------------------")
        print(f"{c.nombre} {c.apellidos}")
        print(f"DNI: {c.dni}")
        print(f"Dirección: {c.direccion}")
        print(f"Provincia: {c.provincia}")
        print(f"Delegación: {c.delegacion_cercana.nombre if c.delegacion_cercana else 'N/A'}")
        print(f"Distancia: {c.distancia_despacho} km")


# ==========================================================
# MENU
# ==========================================================
def menu():

    while True:

        print("\nGESTION CLIENTES")
        print("1 Alta cliente")
        print("2 Baja cliente")
        print("3 Modificar cliente")
        print("4 Listar clientes")
        print("0 Salir")

        op = input("Opcion: ")

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
    menu()