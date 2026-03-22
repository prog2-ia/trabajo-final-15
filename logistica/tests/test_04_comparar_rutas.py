"""
-------------------------------------------------------
- Compara la distancia de dos rutas.
- 1 Genera 2 rutas vacias sin pedidos asignando una distancia aleatoria
- 2 imprime las dos rutas
- 3 Informa de la ruta mas barata
________________________________________________________
"""
import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utiles.utils as utils


if __name__ == "__main__":

    print("=== COMPARAR RUTAS ===")


    utils.test_comparar_rutas()
