"""
_______________________________________
      OPTIMIZAR RUTA BUSCANDO EL CAMINO MAS CORTO
AUTOR: Manuel Quiles
1- Genera pedidos aleatorios
2- Optimiza el orden (vecino más cercano)
3- Construye una ruta
4- Calcula la distancia total
5- Muestra resultados

Se ha implementado un algoritmo heurístico de vecino más cercano para la optimización de rutas logísticas,
minimizando la distancia recorrida entre destinos consecutivos.
-----------------------------------------
"""


import random
from math import radians, sin, cos, sqrt, atan2
import sys
import os
import folium
from pathlib import Path
import webbrowser

# Añadir la carpeta raíz del proyecto al path para poder importar módulos propios
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utiles.utils as utils
from datos.ciudades_alicante import CIUDADES_ALICANTE
from clases.pedido import Pedido
from clases.ruta import Ruta

from datetime import datetime, timedelta


# -----------------------
# GENERAR PEDIDOS
# -----------------------
def generar_pedidos(n=100):
    """
    Genera una lista de n pedidos aleatorios.
    Todos los pedidos tienen origen en Alicante y destino aleatorio.
    """

    pedidos = []

    # Lista de ciudades disponibles (excepto Alicante como destino)
    ciudades = list(CIUDADES_ALICANTE.keys())
    ciudades.remove("Alicante")

    niveles_servicio = ["standard", "urgente"]

    for i in range(n):

        # Origen fijo en Alicante
        origen = "Alicante"

        # Seleccionamos destino aleatorio
        destino = random.choice(ciudades)

        # Evitamos que origen y destino sean iguales
        while destino == origen:
            destino = random.choice(ciudades)

        # Generamos peso y volumen aleatorios
        peso = round(random.uniform(1, 100), 2)
        volumen = round(random.uniform(0.1, 5), 2)

        # Fecha de entrega aleatoria (1 a 10 días)
        fecha = datetime.now() + timedelta(days=random.randint(1, 10))

        # Nivel de servicio aleatorio
        nivel = random.choice(niveles_servicio)

        # Creamos objeto Pedido
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


# -----------------------
# OPTIMIZAR RUTA
# -----------------------
def optimizar_ruta(pedidos):
    """
    Ordena los pedidos utilizando el algoritmo del vecino más cercano.
    Minimiza la distancia recorrida seleccionando en cada paso
    el pedido cuyo destino esté más cerca de la ciudad actual.
    """

    origen = "Alicante"
    ruta_ciudades = [origen]

    pendientes = pedidos.copy()
    actual = origen

    pedidos_ordenados = []

    # Mientras queden pedidos por asignar
    while pendientes:

        # Seleccionamos el pedido cuyo destino está más cerca de la ciudad actual
        siguiente = min(
            pendientes,
            key=lambda p: utils.distancia_km(
                CIUDADES_ALICANTE[actual],
                CIUDADES_ALICANTE[p.destino]
            )
        )

        # Añadimos el pedido a la ruta ordenada
        pedidos_ordenados.append(siguiente)

        # Guardamos la ciudad destino en el recorrido
        ruta_ciudades.append(siguiente.destino)

        # Eliminamos el pedido de pendientes
        pendientes.remove(siguiente)

        # Actualizamos la ciudad actual
        actual = siguiente.destino

    return pedidos_ordenados, ruta_ciudades


# -----------------------
# CREAR RUTA
# -----------------------
def crear_ruta(id_ruta, pedidos_ordenados):
    """
    Crea un objeto Ruta a partir de una lista de pedidos ordenados.
    """

    ruta = Ruta(id_ruta)

    # Asignamos los pedidos a la ruta
    ruta.lista_pedidos = pedidos_ordenados

    return ruta


# -----------------------
# CALCULAR DISTANCIA TOTAL
# -----------------------
def calcular_distancia_ruta(ruta):
    """
    Calcula la distancia total de la ruta sumando las distancias
    entre destinos consecutivos.
    """

    total = 0

    # Recorremos los pedidos de dos en dos
    for i in range(len(ruta.lista_pedidos) - 1):

        p1 = ruta.lista_pedidos[i]
        p2 = ruta.lista_pedidos[i+1]

        # Sumamos la distancia entre destinos consecutivos
        total += utils.distancia_km(
            CIUDADES_ALICANTE[p1.destino],
            CIUDADES_ALICANTE[p2.destino]
        )

    # Guardamos la distancia total en la ruta
    ruta.distancia_total = round(total, 2)

    return ruta.distancia_total

def mapa_ruta_optimizada(ruta_ciudades):
    """
    Dibuja la ruta optimizada en un mapa con líneas entre ciudades.
    """

    # Coordenadas iniciales (centro aproximado)
    mapa = folium.Map(location=[38.5, -0.5], zoom_start=9)

    coordenadas = []

    # Añadimos marcadores
    for i, ciudad in enumerate(ruta_ciudades):

        lat, lon = CIUDADES_ALICANTE[ciudad]
        coordenadas.append((lat, lon))

        folium.Marker(
            location=[lat, lon],
            popup=f"{i+1}. {ciudad}",
            icon=folium.Icon(color="blue" if i != 0 else "green")
        ).add_to(mapa)

    #  DIBUJAR LA RUTA (línea)
    folium.PolyLine(
        locations=coordenadas,
        color="red",
        weight=4,
        opacity=0.8
    ).add_to(mapa)

    # Guardar archivo
    ruta_archivo = Path("datos/ruta.html")
    ruta_archivo.parent.mkdir(exist_ok=True)

    mapa.save(ruta_archivo)

    # Abrir automáticamente
    webbrowser.open_new_tab(ruta_archivo.resolve().as_uri())


# -----------------------
# EJECUCIÓN PRINCIPAL
# -----------------------
if __name__ == "__main__":

    # Generamos pedidos aleatorios
    pedidos = generar_pedidos(20)

    print("PEDIDOS:")
    for p in pedidos:
        print(p)

    total_km = 0

    for p in pedidos:
        total_km += p.km

    print('---------------')
    print(f"Total km: {total_km:.2f}")

    # Optimizamos el orden de los pedidos
    pedidos_ordenados, ruta_ciudades = optimizar_ruta(pedidos)

    print("\nRUTA OPTIMIZADA:")
    print(" → ".join(ruta_ciudades))

    # Creamos objeto ruta
    ruta = crear_ruta("R1", pedidos_ordenados)

    # Calculamos distancia total
    distancia = calcular_distancia_ruta(ruta)

    # Mostramos información de la ruta
    print(ruta)
    print("\nDistancia total:", distancia, "km")

    mapa_ruta_optimizada(ruta_ciudades)