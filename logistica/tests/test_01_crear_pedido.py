"""
-------------------------------------------------------
- crea un pedido.
- 1 Genera 1 pedido
- 3 imprime el pedido utilizando la sobrecarga __str__
________________________________________________________
"""
import sys
import os
import random

from datetime import datetime, timedelta


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clases.pedido import Pedido


def test_crear_pedido():

    print("Test crear pedido")

    fecha = datetime.now() + timedelta(days=2)

    p = Pedido(
        "P1",
        "Alicante",
        "Elche",
        10,
        2,
        fecha,
        "standard"
    )

    # sobrecargamos con __str__ en clase pedido
    print(p)


if __name__ == "__main__":

    print("=== CREAR PEDIDO ===")

    test_crear_pedido()

