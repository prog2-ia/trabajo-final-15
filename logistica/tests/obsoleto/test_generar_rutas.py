import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import utiles.utils as utils

from clases.pedido import Pedido
from clases.ruta import Ruta
from tests.generador_pedidos import generar_pedidos

if __name__ == "__main__":

    pedidos = generar_pedidos(100)

    rutas = utils.generar_rutas(pedidos)

    for i, ruta in enumerate(rutas):
        print(f"\nRuta {i + 1}:")
        for p in ruta:
            print(f"{p.origen} → {p.destino}")
