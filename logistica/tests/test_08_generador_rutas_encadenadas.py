"""
-------------------------------------------------------
AUTOR: Manuel Quiles

- Genera ruta encadenadas.
- 1 Genera 100 pedidos aleatorios
- 2 Genera las rutas encadenando origen y destino
- 3 imprime todas la rutas generadas
________________________________________________________
"""
import sys
import os
from datetime import datetime, timedelta
import random


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.pedido import Pedido
from clases.ruta import Ruta
from datos.ciudades_alicante import CIUDADES_ALICANTE

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

def generar_ruta_encadenada(pedidos):
    """
    Genera una ruta encadenada a partir de una lista de pedidos.
    """

    # Si no hay pedidos, devolvemos lista vacía
    if not pedidos:
        return []

    # Copiamos la lista para no modificar la original
    pendientes = pedidos.copy()

    # Elegimos el primer pedido como inicio de la ruta
    # (en tu comentario dices aleatorio, pero aquí es el primero)
    ruta = [pendientes.pop(0)]

    # Bucle infinito hasta que no encontremos más enlaces
    while True:

        # Último pedido añadido a la ruta
        ultimo = ruta[-1]

        # Flag para saber si hemos encontrado un pedido encadenado
        encontrado = False

        # Buscamos en los pedidos pendientes
        for p in pendientes:

            # Si el origen del pedido coincide con el destino del último
            # entonces podemos encadenarlo
            if p.origen == ultimo.destino:

                # Añadimos el pedido a la ruta
                ruta.append(p)

                # Lo eliminamos de pendientes (ya usado)
                pendientes.remove(p)

                # Marcamos que hemos encontrado uno
                encontrado = True

                # Salimos del bucle (solo cogemos uno cada vez)
                break

        # Si no hemos encontrado ningún pedido que encaje, terminamos
        if not encontrado:
            break

    # Devolvemos la ruta construida
    return ruta


def generar_rutas(pedidos):
    """
    Genera múltiples rutas encadenadas a partir de pedidos.
    """

    # Copiamos la lista original
    pendientes = pedidos.copy()

    # Lista donde guardaremos todas las rutas
    rutas = []

    # Mientras queden pedidos sin asignar
    while pendientes:

        # Creamos una nueva ruta empezando por el primer pedido disponible
        ruta = [pendientes.pop(0)]

        # Intentamos encadenar pedidos a esta ruta
        while True:

            # Último pedido de la ruta actual
            ultimo = ruta[-1]

            # Flag para saber si encontramos un encadenamiento
            encontrado = False

            # Buscamos en los pendientes
            for p in pendientes:

                # Si encaja origen-destino
                if p.origen == ultimo.destino:

                    # Añadimos a la ruta
                    ruta.append(p)

                    # Eliminamos de pendientes
                    pendientes.remove(p)

                    # Marcamos como encontrado
                    encontrado = True

                    # Salimos del bucle
                    break

            # Si no encontramos más enlaces, cerramos esta ruta
            if not encontrado:
                break

        # Guardamos la ruta completa
        rutas.append(ruta)

    # Devolvemos todas las rutas generadas
    return rutas

import folium
from pathlib import Path
import webbrowser


if __name__ == "__main__":

    pedidos = generar_pedidos(100)

    rutas = generar_rutas(pedidos)

    for i, ruta in enumerate(rutas):
        print(f"\nRuta {i+1}:")
        for p in ruta:
            print(f"{p.origen} → {p.destino}")

    print()
    print()
    ruta=generar_ruta_encadenada(pedidos)
    for p in ruta:
        print(f"{p.origen} → {p.destino}")

