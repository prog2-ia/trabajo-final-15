import os
import sys

# asegurar acceso a la raiz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)


def menu_pedidos():

    while True:

        print("\n" + "=" * 40)
        print("        GESTION DE PEDIDOS")
        print("=" * 40)

        print("1. Gestion de pedidos")
        print("2. Informes de pedidos")
        print("0. Volver")

        opcion = input("\nSeleccione una opcion: ").strip()

        if opcion == "1":
            ejecutar_gestion_pedidos()

        elif opcion == "2":
            ejecutar_informes_pedidos()

        elif opcion == "0":
            break

        else:
            print("Opcion no valida")


# ==========================================
# FUNCIONES DE EJECUCION
# ==========================================

def ejecutar_gestion_pedidos():
    from programas.pedidos.gestion_de_pedidos import menu_gestion_pedidos
    menu_gestion_pedidos()


def ejecutar_informes_pedidos():
    from programas.pedidos.informes_de_pedidos import menu_informes_pedidos
    menu_informes_pedidos()