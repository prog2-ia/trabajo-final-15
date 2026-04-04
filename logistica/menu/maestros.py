import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

import os
import sys

# asegurar acceso a la raiz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)


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

        if opcion == "1":
            ejecutar_clientes()

        elif opcion == "2":
            ejecutar_delegaciones()

        elif opcion == "3":
            ejecutar_vehiculos()

        elif opcion == "0":
            break

        else:
            print("Opcion no valida")


# ==========================================
# FUNCIONES DE EJECUCION
# ==========================================

def ejecutar_clientes():
    from programas.maestros.mantenimiento_de_clientes import menu_clientes
    menu_clientes()


def ejecutar_delegaciones():
    from programas.maestros.mantenimiento_de_delegaciones import menu_delegaciones
    menu_delegaciones()


def ejecutar_vehiculos():
    from programas.maestros.mantenimiento_de_vehiculos import menu_vehiculos
    menu_vehiculos()