"""
-------------------------------------------------------
- Suma 2 pedidos.
- 1 Genera 2 pedidos
- 2 Imprime los dos pedidos utilizando la sobrecarga __str__ de la clase pedido
- 3 Genera un nuevo pedido utilizando la sobrecarga __add__ de la clase pedido
- 4 imprime el nuevo pedido suma
________________________________________________________
"""
import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utiles.utils as utils


if __name__ == "__main__":
    print("=== SUMAR PEDIDOS P1 y P2 ===")

    utils.test_sumar_pedidos()