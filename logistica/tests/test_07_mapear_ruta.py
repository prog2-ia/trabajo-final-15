"""
-------------------------------------------------------
- Mapea los origenes de cada pedido en un mapa.
- 1 Genera 10 pedidos aleatorios
- 2 Genera una ruta a partir de los 10 pedidos
- 3 imprime la ruta (utiliza la sobrecarga __str__ de la clase ruta)
- 4 Dibuja los origenes de cada pedido de la ruta en un mapa por medio de la libreria folium
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

    utils.mapa_ruta(ruta)
    print("Se ha generado el mapa en 'datos/ruta.html'")

