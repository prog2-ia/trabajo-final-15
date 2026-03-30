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
from datetime import datetime, timedelta


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from clases.ruta import Ruta
from clases.pedido import Pedido



def test_ruta():

    print("\nTest ruta")

    fecha = datetime.now() + timedelta(days=3)

    p1 = Pedido("P1", "Alicante", "Valencia", 5, 1, fecha, "standard")
    p2 = Pedido("P2", "Valencia", "Madrid", 8, 2, fecha, "standard")

    r = Ruta("R1", 200)

    r.agregar_pedido(p1)
    r.agregar_pedido(p2)

    print(r)


if __name__ == "__main__":

    print("=== CREAR RUTA A PARTIR DE VARIOS PEDIDOS ===")
    test_ruta()

