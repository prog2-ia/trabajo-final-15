import random
from datetime import datetime, timedelta
from logistica.clases.pedido import Pedido

ciudades = [
    "Alicante", "Valencia", "Madrid", "Barcelona",
    "Murcia", "Sevilla", "Bilbao", "Zaragoza"
]

niveles_servicio = ["standard", "urgente"]


def generar_pedidos(n=100):

    pedidos = []

    for i in range(n):

        origen = random.choice(ciudades)
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