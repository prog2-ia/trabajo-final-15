


import sys
import os


# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import matplotlib.pyplot as plt
import folium


from datetime import datetime, timedelta
from clases.pedido import Pedido
from clases.ruta import Ruta
from tests.generador_pedidos import generar_pedidos


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

    print(p)


def test_error_peso():

    print("\nTest error peso")

    try:

        fecha = datetime.now() + timedelta(days=2)

        Pedido(
            "P2",
            "Alicante",
            "Madrid",
            -5,
            2,
            fecha,
            "standard"
        )

    except ValueError as e:
        print("Error detectado correctamente:", e)


def test_sumar_pedidos():

    print("\nTest sumar pedidos")

    fecha = datetime.now() + timedelta(days=3)

    p1 = Pedido("P1", "Alicante", "Valencia", 5, 1, fecha, "standard")
    p2 = Pedido("P2", "Valencia", "Madrid", 8, 2, fecha, "standard")

    p3 = p1 + p2

    print("Pedido combinado:")
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

    print("Peso total:", r.peso_total())
    print("Volumen total:", r.volumen_total())
    print("Coste:", r.calcular_coste())
"""
    print()
    print(r.generar_albaran_ruta())
    r = Ruta(200)

    r.agregar_pedido(p1)
    r.agregar_pedido(p2)

    r.distancia_total = 200

    print(r)
    # print("Coste:", r.calcular_coste(),"Peso:",r.peso_total())
    print(f'Coste:{r.calcular_coste()}  Peso:{r.peso_total()}')
"""

def test_comparar_rutas():

    print("\nTest comparar rutas")

    r1 = Ruta("R1")
    r2 = Ruta("R2")

    r1.distancia_total = 100
    r2.distancia_total = 200

    if r1 < r2:
        print("Ruta 1 es más barata")
    else:
        print("Ruta 2 es más barata")




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

    mapa.save("ruta.html")

if __name__ == "__main__":

    print("=== VALIDACIÓN DE CLASES ===")

    test_crear_pedido()
    test_error_peso()
    test_sumar_pedidos()
    test_ruta()
    test_comparar_rutas()

    pedidos = generar_pedidos(100)

    print("Pedidos generados:", len(pedidos))
    print(pedidos[0])
    for p in pedidos:
        print(p)


    ruta = Ruta("R1", 200)

    for p in pedidos[:10]:
        ruta.agregar_pedido(p)

    print(ruta)

    dibujar_ruta(ruta)
    mapa_ruta(ruta)