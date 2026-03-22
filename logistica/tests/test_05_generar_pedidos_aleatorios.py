"""
-------------------------------------------------------
- Genera pedidos aleatorios.
- 1 Genera 100 pedidos aleatorios
- 2 Imprime todos los pedidos generados
________________________________________________________
"""
import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utiles.utils as utils

if __name__ == "__main__":

    print("=== GENERAR 100 pedidos aleatorios ===")



    pedidos = utils.generar_pedidos(100)

    print("Pedidos generados:", len(pedidos))
    print(pedidos[0])
    for p in pedidos:
        print(p)