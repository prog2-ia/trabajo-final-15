# menu/menu_principal.py

import os
import sys

# asegurar acceso a la raiz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

# importar submenus
from menu.maestros import menu_maestros
# from menu.pedidos import menu_pedidos
# from menu.rutas import menu_rutas


def menu_principal():

    while True:

        print("\n" + "=" * 40)
        print("   SISTEMA DE GESTION LOGISTICA")
        print("=" * 40)

        print("1. Gestion de archivos maestros")
        print("2. Gestion de pedidos")
        print("3. Gestion de rutas")
        print("0. Salir")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            menu_maestros()

        elif opcion == "2":
            menu_pedidos()

        elif opcion == "3":
            menu_rutas()

        elif opcion == "0":
            print("\nSaliendo de la aplicacion...")
            break

        else:
            print("Opcion no valida")