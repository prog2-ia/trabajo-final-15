import sys
import os

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, timedelta
from logistica.clases.pedido import Pedido
from logistica.clases.ruta import Ruta


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

    r = Ruta(200)

    r.agregar_pedido(p1)
    r.agregar_pedido(p2)

    r.distancia_total = 200

    print(r)
    print("Coste:", r.calcular_coste())


def test_comparar_rutas():

    print("\nTest comparar rutas")

    r1 = Ruta()
    r2 = Ruta()

    r1.distancia_total = 100
    r2.distancia_total = 200

    if r1 < r2:
        print("Ruta 1 es más barata")
    else:
        print("Ruta 2 es más barata")


if __name__ == "__main__":

    print("=== VALIDACIÓN DE CLASES ===")

    test_crear_pedido()
    test_error_peso()
    test_sumar_pedidos()
    test_ruta()
    test_comparar_rutas()