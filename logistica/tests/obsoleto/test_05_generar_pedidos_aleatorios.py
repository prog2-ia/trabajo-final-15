"""
-------------------------------------------------------
- Genera pedidos aleatorios.
- 1 Genera 100 pedidos aleatorios
- 2 Imprime todos los pedidos generados
________________________________________________________
"""
import os
import random
import sys
from datetime import datetime, timedelta

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from datos.dic_ciudades_alicante import CIUDADES_ALICANTE

from clases.pedido import Pedido


def generar_pedidos(n=100):
    pedidos = []
    ciudades = list(CIUDADES_ALICANTE.keys())
    niveles_servicio = ["standard", "urgente"]

    for i in range(n):

        # elegir ciudades aleatorias
        origen = random.choice(ciudades)
        destino = random.choice(ciudades)

        # evitar origen y destino iguales
        while destino == origen:
            destino = random.choice(ciudades)

        peso = round(random.uniform(1, 100), 2)
        volumen = round(random.uniform(0.1, 5), 2)

        fecha = datetime.now() + timedelta(days=random.randint(1, 10))

        nivel = random.choice(niveles_servicio)

        p = Pedido(
            f"P{i}",
            origen,
            destino,
            peso,
            volumen,
            fecha,
            nivel
        )

        pedidos.append(p)

    return pedidos


if __name__ == "__main__":

    print("=== GENERAR 100 pedidos aleatorios ===")

    pedidos = generar_pedidos(100)

    print("Pedidos generados:", len(pedidos))
    print(pedidos[0])
    for p in pedidos:
        print(p)
