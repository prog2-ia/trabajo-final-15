import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(BASE_DIR)

import os
import sys

# asegurar acceso a la raiz del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.append(BASE_DIR)




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