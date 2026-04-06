# menu/menu_principal.py

import os
import sys

# asegurar acceso a la raiz del proyecto
# BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.append(BASE_DIR)

from tests.test_15_prueba_delegaciones import ejecutar as test_delegaciones
from tests.test_10_generar_clientes_aleatorios import ejecutar as test_clientes



def menu_datos_prueba():
    while True:
        print("\n" + "=" * 40)
        print("   GENERACION DE DATOS DE PRUEBA")
        print("=" * 40)

        print("1. Generación de delegaciones de prueba y cache de geolocaciones")
        print("2. Generación de clientes de prueba y caché de geolocaciones")
        print("3. Generación de pedidos de prueba")
        print("-" * 40)
        print("4. Generación de vehículos de prueba y flotas" )
        print("0. Volver")

        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            test_delegaciones()
        elif opcion == "2":
            test_clientes()
        # elif opcion == "3":
            # test_17_prueba_pedidos.py
        # elif opcion == "4":
            # test_18_prueba_vehículos.py
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")

def menu_maestros():
    while True:

        print("\n" + "=" * 40)
        print("   GESTION DE ARCHIVOS MAESTROS")
        print("=" * 40)

        print("1. Mantenimiento de clientes")
        print("2. Mantenimiento de delegaciones")
        print("3. Mantenimiento de vehiculos")
        print("0. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        # if opcion == "1":
            # ejecutar_clientes()
        # elif opcion == "2":
            # ejecutar_delegaciones()

        # elif opcion == "3":
            # ejecutar_vehiculos()

        if opcion == "0":
            break

        else:
            print("Opcion no valida")

def menu_pedidos():
    while True:

        print("\n" + "=" * 40)
        print("   GESTION DE PEDIDOS")
        print("=" * 40)

        print("1. Mantenimiento de pedidos")
        print("2. Busqueda de pedidos")
        print("3. Informe de pedidos")
        print("0. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        # if opcion == "1":
            # mantenimiento_pedidos.py()

        # elif opcion == "2":
            # busqueda_pedidos.py

        # elif opcion == "3":
            # inform_pedidos.py()

        if opcion == "0":
            break

        else:
            print("Opcion no valida")

def menu_rutas():
    while True:

        print("\n" + "=" * 40)
        print("   GESTION DE RUTAS")
        print("=" * 40)

        print("1. Generar rutas de recogida")
        print("2. Generar rutas de transporte")
        print("3. Generar rutas de reparto")
        print("4. Consultar estado de flotas")
        print("0. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        # if opcion == "1":
            # generar_rutas_recogida.py()

        # elif opcion == "2":
            # generar_rutas_transporte.py()

        # elif opcion == "3":
            # generar_rutas_reparto.py()

        # elif opcion == "4":
            # consultar_flotas.py()

        if opcion == "0":
            break

        else:
            print("Opcion no valida")


def menu_principal():

    while True:

        print("\n" + "=" * 40)
        print("   SISTEMA DE GESTION LOGISTICA")
        print("=" * 40)

        print("1. Gestion de archivos maestros")
        print("2. Gestion de pedidos")
        print("3. Gestion de rutas")
        print("4. Generación de datos de prueba")
        print("0. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            menu_maestros()

        elif opcion == "2":
            menu_pedidos()

        elif opcion == "3":
            menu_rutas()

        elif opcion =='4':
            menu_datos_prueba()

        elif opcion == "0":
            print("\nSaliendo de la aplicacion...")
            break

        else:
            print("Opcion no valida")