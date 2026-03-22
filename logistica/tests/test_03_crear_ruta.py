"""
-------------------------------------------------------
- Genera una ruta a partir de 2 pedidos
- 1 Genera 2 pedidos
- 2 Genera una ruta con los 2 pedidos generados
- 3 Imprime la ruta, incluido el albaran, utilizando la sobrecarga __str__ de la clase ruta
________________________________________________________
"""

import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utiles.utils as utils


if __name__ == "__main__":

    print("=== CREAR RUTA A PARTIR DE VARIOS PEDIDOS ===")
    utils.test_ruta()

