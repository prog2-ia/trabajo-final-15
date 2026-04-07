import os
import random
import sys

# añadir raiz del proyecto correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

"""
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
sys.path.append(BASE_DIR)
"""

from clases.cliente import Cliente
from clases.direccion import Direccion
import utiles.utils as utils
from persistencia.persistencia_clientes import (
    guardar_clientes,
    cargar_clientes
)

# ==========================================
# DATOS BASE
# ==========================================

nombres = [
    "Juan", "Maria", "Luis", "Ana", "Pedro", "Lucia",
    "Carlos", "Elena", "Miguel", "Carmen"
]

apellidos = [
    "Garcia", "Perez", "Lopez", "Sanchez", "Martinez",
    "Gomez", "Fernandez", "Ruiz", "Diaz", "Moreno"
]

# ==========================================
# DIRECCIONES REALES
# ==========================================

direcciones_validas = [
    ("España", "Alicante", "Alicante", "Avenida Maisonnave", 1, (38.3452, -0.4810)),
    ("España", "Alicante", "Elche", "Avenida Libertad", 20, (38.2669, -0.6983)),
    ("España", "Alicante", "Benidorm", "Avenida Mediterraneo", 30, (38.5365, -0.1300)),
    ("España", "Madrid", "Madrid", "Gran Via", 1, (40.4193, -3.7058)),
    ("España", "Madrid", "Madrid", "Calle Alcala", 50, (40.4200, -3.6880)),
]


# ==========================================
# FUNCIONES
# ==========================================


def generar_direccion():
    d = random.choice(direcciones_validas)

    return Direccion(
        pais=d[0],
        provincia=d[1],
        ciudad=d[2],
        calle=d[3],
        numero=d[4]
    )


def generar_cliente():
    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)

    while apellido2 == apellido1:
        apellido2 = random.choice(apellidos)

    return Cliente(
        dni=utils.generar_dni_real(),
        nombre=random.choice(nombres),
        apellidos=f"{apellido1} {apellido2}",
        direccion=generar_direccion()
    )


# ==========================================
# CRUD
# ==========================================

clientes = cargar_clientes()


def alta_cliente_interactiva():
    print("\n--- ALTA CLIENTE ---")

    # valores iniciales
    dni = ""
    nombre = ""
    apellido1 = ""
    apellido2 = ""
    pais = "España"
    provincia = "Alicante"
    ciudad = ""
    calle = ""
    numero = ""

    while True:

        print("\nIntroduce los datos (Enter mantiene valor actual)\n")

        # ==========================
        # VALIDACION DNI
        # ==========================
        while True:

            dni_input = input(f"DNI [{dni}]: ") or dni

            c_temp = Cliente(dni_input, nombre, "", None)

            if not c_temp.validar_dni():
                print("DNI invalido")
                continue

            if dni_input in clientes:
                print("El cliente ya existe")
                continue

            dni = dni_input
            break

        # datos personales
        nombre = input(f"Nombre [{nombre}]: ") or nombre
        apellido1 = input(f"Primer apellido [{apellido1}]: ") or apellido1
        apellido2 = input(f"Segundo apellido [{apellido2}]: ") or apellido2

        pais = input(f"Pais [{pais}]: ") or pais
        provincia = input(f"Provincia [{provincia}]: ") or provincia

        # ==========================
        # VALIDACION DIRECCION
        # ==========================
        while True:

            ciudad = input(f"Ciudad [{ciudad}]: ") or ciudad
            calle = input(f"Calle [{calle}]: ") or calle
            numero = input(f"Numero [{numero}]: ") or numero

            # validar numero
            if not str(numero).isdigit():
                print("Numero invalido")
                continue

            numero_int = int(numero)

            direccion = Direccion(pais, provincia, ciudad, calle, numero_int)

            # validar direccion real con geopy
            if not direccion.validar():
                print("Direccion no valida, vuelva a introducirla")
                continue

            break  # direccion correcta

        # crear cliente definitivo
        c = Cliente(dni, nombre, f"{apellido1} {apellido2}", direccion)

        # resumen
        print("\nResumen:")
        print(f"{dni} | {apellido1} {apellido2} {nombre}")
        print(f"{calle} {numero}, {ciudad}, {provincia}, {pais}")

        confirmacion = input("Confirmar alta (s/n): ")

        if confirmacion.lower() == "s":
            clientes[dni] = c
            guardar_clientes(clientes)
            print("Cliente añadido correctamente")
            break
        else:
            print("Alta cancelada")
            break


def baja_cliente_interactiva():
    print("\n--- BAJA CLIENTE ---")

    if not clientes:
        print("No hay clientes")
        return

    # ==========================
    # BUSQUEDA POR APELLIDOS
    # ==========================
    apellidos_buscar = input("Apellidos a buscar: ").strip()

    coincidencias = [
        c for c in clientes.values()
        if apellidos_buscar.lower() in c.apellidos.lower()
    ]

    if not coincidencias:
        print("No se encontraron clientes")
        return

    # ordenar por apellidos y nombre
    coincidencias.sort(key=lambda c: (c.apellidos, c.nombre))

    print("\nClientes encontrados:\n")

    for c in coincidencias:
        print(f"{c.dni} | {c.apellidos}, {c.nombre}")

    # ==========================
    # SELECCION DNI
    # ==========================
    dni_default = coincidencias[0].dni

    dni = input(f"\nDNI [{dni_default}]: ").strip() or dni_default

    if dni not in clientes:
        print("DNI no encontrado")
        return

    c = clientes[dni]
    # ==========================
    # CONFIRMACION
    # ==========================
    print("\nCliente a eliminar:")
    # print(f"{c.dni} | {c.apellidos} {c.nombre} | {c.direccion}")

    d = c.direccion

    direccion_txt = (
        f"{utils.limpiar_texto(d._calle)} {d._numero}, "
        f"{utils.limpiar_texto(d._ciudad)}, "
        f"{utils.limpiar_texto(d._provincia)}, "
        f"{utils.limpiar_texto(d._pais)}"
    )

    print("\nCliente a eliminar:")
    print(f"{c.dni} | {c.apellidos} {c.nombre} | {direccion_txt}")

    confirmacion = input("Confirmar baja (s/n): ")

    if confirmacion.lower() != "s":
        print("Baja cancelada")
        return

    # ==========================
    # ELIMINAR
    # ==========================
    del clientes[dni]

    guardar_clientes(clientes)

    print("Cliente eliminado correctamente")


def modificar_cliente_interactiva():
    print("\n--- MODIFICAR CLIENTE ---")

    if not clientes:
        print("No hay clientes")
        return

    # ==========================
    # BUSQUEDA POR APELLIDOS
    # ==========================
    apellidos_buscar = input("Apellidos a modificar: ").strip()

    coincidencias = [
        c for c in clientes.values()
        if apellidos_buscar.lower() in c.apellidos.lower()
    ]

    if not coincidencias:
        print("No se encontraron clientes")
        return

    # ordenar
    coincidencias.sort(key=lambda c: (c.apellidos, c.nombre))

    print("\nClientes encontrados:\n")

    for c in coincidencias:
        print(f"{c.dni} | {c.apellidos} {c.nombre}")

    # ==========================
    # DNI POR DEFECTO (PRIMERO)
    # ==========================
    dni_default = coincidencias[0].dni

    print(f"\nDNI por defecto: {dni_default}")

    dni = input(f"Seleccione DNI [{dni_default}]: ").strip() or dni_default

    if dni not in clientes:
        print("DNI no encontrado")
        return

    c = clientes[dni]
    d = c.direccion

    # ==========================
    # MOSTRAR DATOS ACTUALES
    # ==========================
    def limpiar(txt):
        return str(txt).replace("'", "").replace('"', "")

    print("\nDatos actuales:")
    print(f"{c.dni} | {c.apellidos} {c.nombre}")
    print(f"{limpiar(d._calle)} {d._numero}, {limpiar(d._ciudad)}, {limpiar(d._provincia)}, {limpiar(d._pais)}")

    # ==========================
    # MODIFICAR DATOS PERSONALES
    # ==========================
    nombre = input(f"Nombre [{c.nombre}]: ") or c.nombre

    apellido1, *resto = c.apellidos.split()
    apellido2 = resto[0] if resto else ""

    apellido1 = input(f"Primer apellido [{apellido1}]: ") or apellido1
    apellido2 = input(f"Segundo apellido [{apellido2}]: ") or apellido2

    pais = input(f"Pais [{d._pais}]: ") or d._pais
    provincia = input(f"Provincia [{d._provincia}]: ") or d._provincia

    # ==========================
    # VALIDACION DIRECCION
    # ==========================
    ciudad = d._ciudad
    calle = d._calle
    numero = str(d._numero)

    while True:

        ciudad = input(f"Ciudad [{ciudad}]: ") or ciudad
        calle = input(f"Calle [{calle}]: ") or calle
        numero = input(f"Numero [{numero}]: ") or numero

        if not numero.isdigit():
            print("Numero invalido")
            continue

        numero_int = int(numero)

        direccion_nueva = Direccion(pais, provincia, ciudad, calle, numero_int)

        if not direccion_nueva.validar():
            print("Direccion no valida")
            continue

        break

    # ==========================
    # VALIDACION DNI REAL
    # ==========================
    while True:

        nuevo_dni_input = input(f"DNI [{c.dni}]: ").strip() or c.dni

        if not utils.validar_dni_real(nuevo_dni_input):
            print("DNI invalido")
            continue

        if nuevo_dni_input != c.dni and nuevo_dni_input in clientes:
            print("El DNI ya existe")
            continue

        nuevo_dni = nuevo_dni_input
        break

    # ==========================
    # CONFIRMACION
    # ==========================
    print("\nDatos modificados:")
    print(f"{nuevo_dni} | {apellido1} {apellido2} {nombre}")
    print(f"{calle} {numero}, {ciudad}, {provincia}, {pais}")

    confirmacion = input("Confirmar modificacion (s/n): ")

    if confirmacion.lower() != "s":
        print("Modificacion cancelada")
        return

    # ==========================
    # APLICAR CAMBIOS
    # ==========================
    if nuevo_dni != c.dni:
        del clientes[c.dni]

    c._dni = nuevo_dni
    c._nombre = nombre
    c._apellidos = f"{apellido1} {apellido2}"
    c._direccion = direccion_nueva

    clientes[nuevo_dni] = c

    guardar_clientes(clientes)

    print("Cliente modificado correctamente")


def listar_clientes():
    if not clientes:
        print("No hay clientes")
        return

    # ordenar por apellidos y nombre
    clientes_ordenados = sorted(
        clientes.values(),
        key=lambda c: (c.apellidos, c.nombre)
    )

    for c in clientes_ordenados:
        d = c.direccion

        # direccion SIN coordenadas
        direccion_txt = f"{d._calle} {d._numero}, {d._ciudad}, {d._provincia}, {d._pais}"

        # pedidos
        pedidos_curso = [p.id for p in c._pedidos_en_curso]
        pedidos_terminados = [p.id for p in c._pedidos_terminados]

        print(
            f"{c.dni} | {c.apellidos} {c.nombre} | {direccion_txt} | "
            f"En curso: {pedidos_curso} | Terminados: {pedidos_terminados}"
        )


def generar_clientes(n=50):
    for _ in range(n):
        c = generar_cliente()
        clientes[c.dni] = c

    print("Numero de clientes:", len(clientes))

    # guardar automaticamente
    guardar_clientes(clientes)


# ==========================================
# MENU
# ==========================================

def menu():
    while True:

        print("\nGESTION CLIENTES")
        print("1 Alta cliente")
        print("2 Baja cliente")
        print("3 Modificar cliente")
        print("4 Listar clientes")
        print("5 Generar 50 clientes")
        print("0 Salir")

        op = input("Opcion: ")
        if op == "1":
            alta_cliente_interactiva()

        elif op == "2":
            baja_cliente_interactiva()

        elif op == "3":
            # dni = input("DNI: ")
            # nombre = input("Nombre: ")
            # apellidos = input("Apellidos: ")
            modificar_cliente_interactiva()

        elif op == "4":
            listar_clientes()

        elif op == "5":
            generar_clientes()

        elif op == "0":
            break


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":
    menu()
