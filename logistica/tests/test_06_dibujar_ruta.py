"""
-------------------------------------------------------
- Dibuja una ruta que une los origenes de cada pedido.
- 1 Genera 10 pedidos aleatorios
- 2 Genera una ruta utilizando los 10 pedidos generados
- 3 Une los origenes de cada pedidos generados mediante coordenadas x,y  ficticias generada aleatoriamente
- 3 imprime la rutas generada
- 4 dibuja la ruta utiliando la libreria matplotlib
________________________________________________________
"""
import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utiles.utils as utils
from clases.ruta import Ruta


if __name__ == "__main__":
    pedidos = utils.generar_pedidos(10)

    print("Pedidos generados:", len(pedidos))
    print(pedidos[0])
    for p in pedidos:
        print(p)


    ruta = Ruta("R1", 200)

    for p in pedidos:
        ruta.agregar_pedido(p)

    print()
    print()
    print(ruta)

    utils.dibujar_ruta(ruta)
