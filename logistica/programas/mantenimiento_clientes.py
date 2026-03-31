"""
==========================================================
PROGRAMA: GESTIÓN DE CLIENTES (CRUD + GENERACIÓN AUTOMÁTICA)
==========================================================

Este programa permite gestionar clientes dentro de una aplicación logística.

FUNCIONALIDADES PRINCIPALES:
---------------------------
1. Alta de clientes (introducción interactiva con validación)
2. Baja de clientes (búsqueda por apellidos + eliminación)
3. Modificación de clientes (edición completa con validaciones)
4. Listado de clientes (ordenados, mostrando pedidos asociados)
5. Generación automática de clientes aleatorios

CARACTERÍSTICAS IMPORTANTES:
---------------------------
- Persistencia de datos (guardar/cargar clientes desde fichero)
- Validación de DNI (realista)
- Validación de direcciones (usando geopy a través de la clase Direccion)
- Uso de estructuras tipo diccionario (clientes[dni] = Cliente)
- Interfaz por consola tipo menú

ESTRUCTURA GENERAL:
-------------------
- DATOS BASE (nombres, apellidos, direcciones)
- FUNCIONES DE GENERACIÓN (clientes y direcciones)
- CRUD (alta, baja, modificación, listado)
- MENÚ PRINCIPAL
"""

import random
import string
import sys
import os

# ==========================================================
# CONFIGURACIÓN DE RUTAS
# ==========================================================
# Añade la raíz del proyecto al PATH para poder importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Alternativa comentada (subir dos niveles)
"""
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..')
)
sys.path.append(BASE_DIR)
"""

# ==========================================================
# IMPORTACIONES DEL PROYECTO
# ==========================================================
from clases.cliente import Cliente
from clases.direccion import Direccion
import utiles.utils as utils
from persistencia.persistencia_clientes import (
    guardar_clientes,
    cargar_clientes
)

# ==========================================================
# DATOS BASE (para generación aleatoria)
# ==========================================================

# Lista de nombres
nombres = [
    "Juan", "Maria", "Luis", "Ana", "Pedro", "Lucia",
    "Carlos", "Elena", "Miguel", "Carmen"
]

# Lista de apellidos
apellidos = [
    "Garcia", "Perez", "Lopez", "Sanchez", "Martinez",
    "Gomez", "Fernandez", "Ruiz", "Diaz", "Moreno"
]

# ==========================================================
# DIRECCIONES REALES (simulación + geolocalización)
# ==========================================================
direcciones_validas = [
    ("España", "Alicante", "Alicante", "Avenida Maisonnave", 1, (38.3452, -0.4810)),
    ("España", "Alicante", "Elche", "Avenida Libertad", 20, (38.2669, -0.6983)),
    ("España", "Alicante", "Benidorm", "Avenida Mediterraneo", 30, (38.5365, -0.1300)),
    ("España", "Madrid", "Madrid", "Gran Via", 1, (40.4193, -3.7058)),
    ("España", "Madrid", "Madrid", "Calle Alcala", 50, (40.4200, -3.6880)),
]

# ==========================================================
# FUNCIONES DE GENERACIÓN
# ==========================================================

def generar_direccion():
    """
    Selecciona una dirección aleatoria de la lista y crea
    un objeto Direccion (sin incluir coordenadas explícitas).
    """
    d = random.choice(direcciones_validas)

    return Direccion(
        pais=d[0],
        provincia=d[1],
        ciudad=d[2],
        calle=d[3],
        numero=d[4]
    )


def generar_cliente():
    """
    Genera un cliente aleatorio:
    - Nombre y apellidos aleatorios
    - DNI válido generado automáticamente
    - Dirección aleatoria válida
    """

    apellido1 = random.choice(apellidos)
    apellido2 = random.choice(apellidos)

    # Evitar repetir el mismo apellido
    while apellido2 == apellido1:
        apellido2 = random.choice(apellidos)

    return Cliente(
        dni=utils.generar_dni_real(),
        nombre=random.choice(nombres),
        apellidos=f"{apellido1} {apellido2}",
        direccion=generar_direccion()
    )


# ==========================================================
# CARGA INICIAL DE CLIENTES (persistencia)
# ==========================================================
clientes = cargar_clientes()


# ==========================================================
# CRUD: ALTA CLIENTE
# ==========================================================

def alta_cliente_interactiva():
    """
    Permite introducir un cliente por consola:
    - Valida DNI
    - Valida dirección real
    - Permite modificar campos antes de confirmar
    """

    print("\n--- ALTA CLIENTE ---")

    # valores iniciales (permite reutilizar inputs)
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

        # ------------------------------
        # VALIDACIÓN DNI
        # ------------------------------
        while True:

            dni_input = input(f"DNI [{dni}]: ") or dni

            # cliente temporal para validar DNI
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

        # ------------------------------
        # VALIDACIÓN DIRECCIÓN
        # ------------------------------
        while True:

            ciudad = input(f"Ciudad [{ciudad}]: ") or ciudad
            calle = input(f"Calle [{calle}]: ") or calle
            numero = input(f"Numero [{numero}]: ") or numero

            # validar que sea numérico
            if not str(numero).isdigit():
                print("Numero invalido")
                continue

            numero_int = int(numero)

            direccion = Direccion(pais, provincia, ciudad, calle, numero_int)

            # validación real (geopy)
            if not direccion.validar():
                print("Direccion no valida, vuelva a introducirla")
                continue

            break

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


# ==========================================================
# CRUD: BAJA CLIENTE
# ==========================================================

def baja_cliente_interactiva():
    """
    Permite eliminar un cliente:
    - Búsqueda por apellidos
    - Selección por DNI
    - Confirmación antes de borrar
    """

    print("\n--- BAJA CLIENTE ---")

    if not clientes:
        print("No hay clientes")
        return

    # búsqueda por apellidos
    apellidos_buscar = input("Apellidos a buscar: ").strip()

    coincidencias = [
        c for c in clientes.values()
        if apellidos_buscar.lower() in c.apellidos.lower()
    ]

    if not coincidencias:
        print("No se encontraron clientes")
        return

    # ordenar resultados
    coincidencias.sort(key=lambda c: (c.apellidos, c.nombre))

    print("\nClientes encontrados:\n")

    for c in coincidencias:
        print(f"{c.dni} | {c.apellidos}, {c.nombre}")

    # selección por DNI
    dni_default = coincidencias[0].dni
    dni = input(f"\nDNI [{dni_default}]: ").strip() or dni_default

    if dni not in clientes:
        print("DNI no encontrado")
        return

    c = clientes[dni]
    d = c.direccion

    # formateo limpio de dirección
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

    # eliminar
    del clientes[dni]
    guardar_clientes(clientes)

    print("Cliente eliminado correctamente")


# ==========================================================
# CRUD: MODIFICAR CLIENTE
# ==========================================================

def modificar_cliente_interactiva():
    """
    Permite modificar un cliente:
    - Búsqueda por apellidos
    - Edición de todos los campos
    - Validación de DNI y dirección
    """

    print("\n--- MODIFICAR CLIENTE ---")

    if not clientes:
        print("No hay clientes")
        return

    apellidos_buscar = input("Apellidos a modificar: ").strip()

    coincidencias = [
        c for c in clientes.values()
        if apellidos_buscar.lower() in c.apellidos.lower()
    ]

    if not coincidencias:
        print("No se encontraron clientes")
        return

    coincidencias.sort(key=lambda c: (c.apellidos, c.nombre))

    for c in coincidencias:
        print(f"{c.dni} | {c.apellidos} {c.nombre}")

    dni_default = coincidencias[0].dni
    dni = input(f"Seleccione DNI [{dni_default}]: ").strip() or dni_default

    if dni not in clientes:
        print("DNI no encontrado")
        return

    c = clientes[dni]
    d = c.direccion

    # mostrar datos actuales
    print("\nDatos actuales:")
    print(f"{c.dni} | {c.apellidos} {c.nombre}")
    print(f"{d._calle} {d._numero}, {d._ciudad}, {d._provincia}, {d._pais}")

    # modificar datos
    nombre = input(f"Nombre [{c.nombre}]: ") or c.nombre

    apellido1, *resto = c.apellidos.split()
    apellido2 = resto[0] if resto else ""

    apellido1 = input(f"Primer apellido [{apellido1}]: ") or apellido1
    apellido2 = input(f"Segundo apellido [{apellido2}]: ") or apellido2

    pais = input(f"Pais [{d._pais}]: ") or d._pais
    provincia = input(f"Provincia [{d._provincia}]: ") or d._provincia

    # validar nueva dirección
    while True:

        ciudad = input(f"Ciudad [{d._ciudad}]: ") or d._ciudad
        calle = input(f"Calle [{d._calle}]: ") or d._calle
        numero = input(f"Numero [{d._numero}]: ") or str(d._numero)

        if not numero.isdigit():
            print("Numero invalido")
            continue

        direccion_nueva = Direccion(pais, provincia, ciudad, calle, int(numero))

        if not direccion_nueva.validar():
            print("Direccion no valida")
            continue

        break

    # validar DNI
    while True:

        nuevo_dni = input(f"DNI [{c.dni}]: ").strip() or c.dni

        if not utils.validar_dni_real(nuevo_dni):
            print("DNI invalido")
            continue

        if nuevo_dni != c.dni and nuevo_dni in clientes:
            print("El DNI ya existe")
            continue

        break

    # confirmación
    print("\nDatos modificados:")
    print(f"{nuevo_dni} | {apellido1} {apellido2} {nombre}")

    if input("Confirmar modificacion (s/n): ").lower() != "s":
        print("Cancelado")
        return

    # aplicar cambios
    if nuevo_dni != c.dni:
        del clientes[c.dni]

    c._dni = nuevo_dni
    c._nombre = nombre
    c._apellidos = f"{apellido1} {apellido2}"
    c._direccion = direccion_nueva

    clientes[nuevo_dni] = c
    guardar_clientes(clientes)

    print("Cliente modificado correctamente")


# ==========================================================
# LISTADO DE CLIENTES
# ==========================================================

def listar_clientes():
    """
    Muestra todos los clientes ordenados:
    - Datos personales
    - Dirección
    - Pedidos asociados
    """

    if not clientes:
        print("No hay clientes")
        return

    clientes_ordenados = sorted(
        clientes.values(),
        key=lambda c: (c.apellidos, c.nombre)
    )

    for c in clientes_ordenados:
        d = c.direccion

        direccion_txt = f"{d._calle} {d._numero}, {d._ciudad}, {d._provincia}, {d._pais}"

        pedidos_curso = [p.id for p in c._pedidos_en_curso]
        pedidos_terminados = [p.id for p in c._pedidos_terminados]

        print(
            f"{c.dni} | {c.apellidos} {c.nombre} | {direccion_txt} | "
            f"En curso: {pedidos_curso} | Terminados: {pedidos_terminados}"
        )


# ==========================================================
# GENERACIÓN AUTOMÁTICA
# ==========================================================

def generar_clientes(n=50):
    """
    Genera n clientes aleatorios y los guarda automáticamente
    """
    for _ in range(n):
        c = generar_cliente()
        clientes[c.dni] = c

    print("Numero de clientes:", len(clientes))
    guardar_clientes(clientes)


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================

def menu():
    """
    Menú interactivo principal del programa
    """

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
            modificar_cliente_interactiva()

        elif op == "4":
            listar_clientes()

        elif op == "5":
            generar_clientes()

        elif op == "0":
            break


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":
    menu()