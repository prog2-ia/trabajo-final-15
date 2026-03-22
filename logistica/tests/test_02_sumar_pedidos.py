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
from datetime import datetime, timedelta



# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from clases.pedido import Pedido

def test_sumar_pedidos():

    print("\nTest sumar pedidos")

    fecha = datetime.now() + timedelta(days=3)

    p1 = Pedido("P1", "Alicante", "Elche", 5, 1, fecha, "standard")
    p2 = Pedido("P2", "Crevillent", "Benidorm", 8, 2, fecha, "standard")

    # Sobrecargamos el + en la clase pedido
    p3 = p1 + p2

    print("Pedido combinado:")
    print(p1)
    print(p2)
    print('.........')
    print(p3)

if __name__ == "__main__":
    print("=== SUMAR PEDIDOS P1 y P2 ===")

    test_sumar_pedidos()