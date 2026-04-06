# suponiendo que tenemos dirección y pedido
import sys
import os
from datetime import datetime, timedelta

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from clases.cliente import Cliente
from clases.direccion import Direccion
from clases.pedido import Pedido

d = Direccion(
    pais="España",
    provincia="Alicante",
    ciudad="Alicante",
    calle="Padre Mariana",
    numero=40
)

# crear cliente
c = Cliente(
    dni="12345678A",
    nombre="Juan",
    apellidos="Perez Lopez",
    direccion=d
)

# validar
c.validar_dni()
c.validar_direccion()

coords = d.obtener_coordenadas()

fecha = datetime.now() + timedelta(days=3)

p1 = Pedido("P1", "Alicante", "Elche", 5, 1, fecha, "standard")
p2 = Pedido("P2", "Crevillent", "Benidorm", 8, 2, fecha, "standard")
# crear pedidos (ejemplo)


# añadir pedidos
c = c + p1
c = c + p2

# terminar pedido
c = c - p1

print(c)