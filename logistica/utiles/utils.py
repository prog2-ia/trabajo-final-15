from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import folium
from pathlib import Path
import webbrowser

# import webbrowser

from clases.pedido import Pedido
from clases.ruta import Ruta
from datos.ciudades import CIUDADES   # importar diccionario de ciudades


def test_crear_pedido():

    print("Test crear pedido")

    fecha = datetime.now() + timedelta(days=2)

    p = Pedido(
        "P1",
        "Alicante",
        "Valencia",
        10,
        2,
        fecha,
        "standard"
    )

    # sobrecargamos con __str__ en clase pedido
    print(p)

def test_sumar_pedidos():

    print("\nTest sumar pedidos")

    fecha = datetime.now() + timedelta(days=3)

    p1 = Pedido("P1", "Alicante", "Valencia", 5, 1, fecha, "standard")
    p2 = Pedido("P2", "Valencia", "Madrid", 8, 2, fecha, "standard")

    # Sobrecargamos el + en la clase pedido
    p3 = p1 + p2

    print("Pedido combinado:")
    print(p1)
    print(p2)
    print('.........')
    print(p3)

def test_ruta():

    print("\nTest ruta")

    fecha = datetime.now() + timedelta(days=3)

    p1 = Pedido("P1", "Alicante", "Valencia", 5, 1, fecha, "standard")
    p2 = Pedido("P2", "Valencia", "Madrid", 8, 2, fecha, "standard")

    r = Ruta("R1", 200)

    r.agregar_pedido(p1)
    r.agregar_pedido(p2)

    print(r)

"""
    print(f"Peso total:{r.peso_total()} kg")
    print(f"Volumen total:{ r.volumen_total()} l")
    print(f"Coste:{r.calcular_coste()} €")
"""

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

def generar_pedidos(n=100):

    pedidos = []
    ciudades = list(CIUDADES.keys())
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
# Dibuja un grajo uniendo coordenadas x,y para cada pedido
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

def mapa_ruta(ruta):

    mapa = folium.Map(location=[40, -3], zoom_start=6)

    for p in ruta.lista_pedidos:
        folium.Marker(
            location=[p.lat, p.lon],
            popup=p.id
        ).add_to(mapa)

    mapa.save("../datos/ruta.html")

    # 🔥 abrir automáticamente
    ruta_archivo = Path("../datos/ruta.html").resolve()

    webbrowser.open_new_tab(ruta_archivo.as_uri())

def generar_ruta_encadenada(pedidos):
    """
    Genera una ruta encadenada a partir de una lista de pedidos.
    """

    if not pedidos:
        return []

    # copiamos lista para no modificar la original
    pendientes = pedidos.copy()

    # elegimos un pedido inicial aleatorio
    ruta = [pendientes.pop(0)]

    while True:

        ultimo = ruta[-1]
        encontrado = False

        for p in pendientes:
            if p.origen == ultimo.destino:
                ruta.append(p)
                pendientes.remove(p)
                encontrado = True
                break

        if not encontrado:
            break

    return ruta

def generar_rutas(pedidos):
    """
    Genera múltiples rutas encadenadas a partir de pedidos.
    """

    pendientes = pedidos.copy()
    rutas = []

    while pendientes:

        ruta = [pendientes.pop(0)]

        while True:

            ultimo = ruta[-1]
            encontrado = False

            for p in pendientes:
                if p.origen == ultimo.destino:
                    ruta.append(p)
                    pendientes.remove(p)
                    encontrado = True
                    break

            if not encontrado:
                break

        rutas.append(ruta)

    return rutas