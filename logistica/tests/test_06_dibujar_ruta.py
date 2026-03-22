"""
-------------------------------------------------------
AUTOR: Manuel Quiles

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
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from datos.ciudades_alicante import CIUDADES_ALICANTE
from clases.ruta import Ruta
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


# Dibuja un grafo uniendo coordenadas x,y para cada pedido
def dibujar_ruta(ruta):

    xs = []
    ys = []

    for p in ruta.lista_pedidos:
        xs.append(p.x)
        ys.append(p.y)

    plt.plot(xs, ys, marker="o")
    plt.title("Ruta logística")
    plt.xlabel("X")
    plt.ylabel("Y")

    for i,p in enumerate(ruta.lista_pedidos):
        plt.text(p.x, p.y, p.id)

    plt.show()

if __name__ == "__main__":
    pedidos = generar_pedidos(10)

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

    dibujar_ruta(ruta)
