"""
-------------------------------------------------------
- Compara la distancia de dos rutas.
- 1 Genera 2 rutas vacias sin pedidos asignando una distancia aleatoria
- 2 imprime las dos rutas
- 3 Informa de la ruta mas barata
________________________________________________________
"""
import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from clases.ruta import Ruta


def test_comparar_rutas():
    print("\nTest comparar rutas")

    r1 = Ruta("R1")
    r2 = Ruta("R2")

    r1.distancia_total = 100
    r2.distancia_total = 200

    print(r1)
    print(r2)
    print()
    print()

    if r1 < r2:
        print("Ruta 1 es más barata")
    else:
        print("Ruta 2 es más barata")


if __name__ == "__main__":
    print("=== COMPARAR RUTAS ===")

    test_comparar_rutas()
