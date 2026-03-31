"""
FICHERO DE TEST DEL SISTEMA LOGÍSTICO

Este script tiene como objetivo comprobar el correcto funcionamiento del sistema
de delegaciones, flotas y vehículos, así como el módulo de persistencia.

FUNCIONALIDAD PRINCIPAL
----------------------
Este programa realiza las siguientes acciones:

1. Configura las rutas de acceso del proyecto para permitir imports entre carpetas.
2. Crea objetos de tipo Delegacion (Central y Despacho).
3. Valida los datos de las delegaciones.
4. Asigna flotas a cada delegación.
5. Crea distintos tipos de vehículos.
6. Añade vehículos a las flotas, comprobando restricciones.
7. Muestra el estado actual del sistema.
8. Guarda las delegaciones en un fichero JSON.
9. Carga las delegaciones desde el fichero.
10. Muestra los datos reconstruidos.

OBJETIVO
--------
Verificar que:
- Las clases funcionan correctamente.
- Las restricciones de negocio se aplican.
- El sistema de persistencia guarda y recupera datos correctamente.

CONCEPTOS APLICADOS
-------------------
- Programación Orientada a Objetos
- Testing funcional
- Persistencia de datos (JSON)
- Gestión de rutas del sistema
"""


# ==========================================================
# CONFIGURACION DE PATH (USANDO UTILS)
# ==========================================================

import sys
import os

# Añadimos al path la carpeta raíz del proyecto
# Esto permite importar módulos entre carpetas sin errores
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

from utiles.utils import encontrar_raiz

# Obtener la ruta base del proyecto
BASE_DIR = encontrar_raiz()

# Añadirla al path si no está ya incluida
if BASE_DIR and BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)


# ==========================================================
# IMPORTS DE CLASES Y FUNCIONES
# ==========================================================

from clases.delegacion import DelegacionCentral, DelegacionDespacho
from clases.vehiculo import (
    VehiculoCamion,
    VehiculoFurgoneta,
    VehiculoMotocicleta,
    VehiculoMochila
)

# Importamos funciones de persistencia
from persistencia.persistencia_delegaciones import (
    guardar_delegaciones,
    cargar_delegaciones
)


# ==========================================================
# CREAR DELEGACIONES
# ==========================================================

# Creamos dos delegaciones: una central y un despacho
central = DelegacionCentral("Central Madrid", "Gran Via 1, Madrid")
despacho = DelegacionDespacho("Despacho Alicante", "Avenida Maisonnave 1, Alicante")

# Validamos nombre y dirección
print("Validar nombre central:", central.validar_nombre())
print("Validar direccion central:", central.validar_direccion())

print("Validar nombre despacho:", despacho.validar_nombre())
print("Validar direccion despacho:", despacho.validar_direccion())


# ==========================================================
# ASIGNAR FLOTAS
# ==========================================================

# Cada delegación obtiene su propia flota de vehículos
central.asignar_flota()
despacho.asignar_flota()


# ==========================================================
# CREAR VEHICULOS
# ==========================================================

# Creamos distintos tipos de vehículos
v1 = VehiculoCamion("1234 ABC")
v2 = VehiculoFurgoneta("5678 DEF")
v3 = VehiculoMotocicleta("1111 GHI")
v4 = VehiculoMochila("Alicante-1")
v5 = VehiculoCamion("2222 JKL", disponible=False)


# ==========================================================
# AÑADIR VEHICULOS A LAS FLOTAS
# ==========================================================

# Probamos añadir vehículos a cada delegación
# Aquí se comprueban restricciones de negocio

print("\n--- CENTRAL ---")
print("Camion:", central.flota.añadir_vehiculo(v1))
print("Furgoneta:", central.flota.añadir_vehiculo(v2))
print("Motocicleta:", central.flota.añadir_vehiculo(v3))
print("Mochila (no permitido):", central.flota.añadir_vehiculo(v4))

print("\n--- DESPACHO ---")
print("Furgoneta:", despacho.flota.añadir_vehiculo(v2))
print("Motocicleta:", despacho.flota.añadir_vehiculo(v3))
print("Mochila:", despacho.flota.añadir_vehiculo(v4))
print("Camion (no permitido):", despacho.flota.añadir_vehiculo(v5))


# ==========================================================
# MOSTRAR ESTADO ACTUAL
# ==========================================================

print("\n--- ESTADO ACTUAL ---")

# Mostrar información de las delegaciones
print(central)
print("Flota central:", central.flota.listar_vehiculos())

print(despacho)
print("Flota despacho:", despacho.flota.listar_vehiculos())


# ==========================================================
# GUARDAR DATOS EN FICHERO
# ==========================================================

print("\nGuardando delegaciones...")

# Guardamos las delegaciones en JSON
guardar_delegaciones([central, despacho])


# ==========================================================
# CARGAR DATOS DESDE FICHERO
# ==========================================================

print("\nCargando delegaciones desde fichero...")

# Recuperamos los datos almacenados
delegaciones = cargar_delegaciones()


# ==========================================================
# MOSTRAR DATOS CARGADOS
# ==========================================================

print("\n--- DELEGACIONES CARGADAS ---")

# Mostramos los objetos reconstruidos
for d in delegaciones:

    print(d)

    # Mostrar vehículos asociados
    if d.flota:
        print("Flota:", d.flota.listar_vehiculos())