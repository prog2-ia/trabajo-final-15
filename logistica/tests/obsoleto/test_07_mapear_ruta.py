"""
-------------------------------------------------------
AUTOR: Manuel Quiles

- Mapea los origenes de cada pedido en un mapa.
- 1 Genera 10 pedidos aleatorios
- 2 Genera una ruta a partir de los 10 pedidos
- 3 imprime la ruta (utiliza la sobrecarga __str__ de la clase ruta)
- 4 Dibuja los origenes de cada pedido de la ruta en un mapa por medio de la libreria folium
________________________________________________________
"""
import os
import random
import sys
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

import folium

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from clases.ruta import Ruta
from clases.pedido import Pedido
from datos.dic_ciudades_alicante import CIUDADES_ALICANTE


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


def mapa_ruta(ruta):
    mapa = folium.Map(location=[40, -3], zoom_start=6)

    for p in ruta.lista_pedidos:
        folium.Marker(
            location=[p.lat, p.lon],
            popup=p.id
        ).add_to(mapa)

    mapa.save("../datos/ruta.html")

    #  abrir automáticamente
    ruta_archivo = Path("../../datos/obsoletos/ruta.html").resolve()

    webbrowser.open_new_tab(ruta_archivo.as_uri())


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

    mapa_ruta(ruta)
    print("Se ha generado el mapa en 'datos/ruta.html'")
