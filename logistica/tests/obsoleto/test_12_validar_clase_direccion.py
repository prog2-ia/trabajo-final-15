# ------------------------------------------
# PROGRAMA DE PRUEBA validacion de direcciones y obtencion de coordenadas
# ---
import os
import sys

# Añadir la carpeta raíz del proyecto al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from clases.direccion import Direccion

# Creamos una dirección real en Alicante
d = Direccion(
    pais="España",
    provincia="Alicante",
    ciudad="Alicante",
    calle="Avenida Maisonnave",
    numero=1
)

# ------------------------------------------
# 1. Mostramos la dirección completa
# ------------------------------------------
print("Dirección:")
print(d.direccion_completa())

# ------------------------------------------
# 2. Validamos si la dirección existe
# ------------------------------------------
valida = d.validar()

if valida:
    print("Dirección válida")
else:
    print("Dirección NO válida")

# ------------------------------------------
# 3. Obtenemos coordenadas
# ------------------------------------------
coords = d.obtener_coordenadas()

if coords:
    print("Coordenadas:", coords)
else:
    print("No se pudieron obtener coordenadas")

# ------------------------------------------
# 4. Mostramos el objeto completo
# ------------------------------------------
print("Objeto completo:")
print(d)
