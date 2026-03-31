"""
MÓDULO DE PERSISTENCIA DE DELEGACIONES Y VEHÍCULOS

Este módulo se encarga de la gestión de la persistencia de datos del sistema logístico,
permitiendo guardar y cargar información de delegaciones y sus flotas de vehículos
en formato JSON.

FUNCIONALIDAD PRINCIPAL
----------------------
El módulo implementa dos procesos fundamentales:

1. SERIALIZACIÓN (GUARDADO)
   Convierte objetos complejos del sistema (delegaciones y vehículos) en estructuras
   de datos simples (diccionarios y listas) que pueden almacenarse en un fichero JSON.

2. DESERIALIZACIÓN (CARGA)
   Lee el fichero JSON y reconstruye los objetos originales del sistema, restaurando
   tanto las delegaciones como sus flotas de vehículos.

ESTRUCTURA DE LOS DATOS
----------------------
Cada delegación se guarda con la siguiente información:
- tipo de delegación (Central o Despacho)
- nombre
- dirección
- coordenadas geográficas
- lista de vehículos asociados

Cada vehículo se guarda como:
- tipo (camión, furgoneta, motocicleta o mochila)
- matrícula
- estado de disponibilidad

FUNCIONES PRINCIPALES
----------------------

crear_vehiculo(tipo, matricula, disponible)
    Implementa un patrón factoría (Factory) para crear dinámicamente el tipo
    de vehículo correspondiente en función del parámetro "tipo".

guardar_delegaciones(delegaciones)
    Convierte la lista de objetos Delegacion en formato JSON y la guarda en
    el fichero "datos/delegaciones.json". Si la carpeta no existe, se crea automáticamente.

cargar_delegaciones()
    Lee el fichero JSON, reconstruye los objetos Delegacion y sus vehículos
    asociados, y devuelve la lista completa de delegaciones del sistema.

DETALLES IMPORTANTES
--------------------
- Se utiliza la función encontrar_raiz() para localizar la ruta base del proyecto,
  garantizando que el sistema funcione independientemente del entorno de ejecución.

- Se emplea JSON como formato de almacenamiento por ser legible, portable
  y fácil de manipular.

- Se utiliza una función factoría para desacoplar la creación de vehículos
  del resto del sistema.

- El sistema reconstruye completamente las relaciones entre objetos
  (delegación → flota → vehículos) al cargar los datos.

CONCEPTOS DE PROGRAMACIÓN APLICADOS
----------------------------------
- Programación Orientada a Objetos (POO)
- Serialización y deserialización de datos
- Patrón de diseño Factory
- Separación de responsabilidades
- Manejo de rutas del sistema (os.path)
- Gestión de ficheros

USO EN EL SISTEMA
----------------
Este módulo permite persistir el estado del sistema logístico entre ejecuciones,
facilitando el almacenamiento y recuperación de datos sin necesidad de bases
de datos externas.

"""


# ==========================================================
# IMPORTACIONES
# ==========================================================

import json        # Para guardar y cargar datos en formato JSON
import sys
import os

# Añadimos al path la carpeta raíz del proyecto para poder importar módulos
# (solución típica cuando hay problemas de imports entre carpetas)
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

# Importamos utilidades y clases necesarias
from utiles.utils import encontrar_raiz
from clases.delegacion import DelegacionCentral, DelegacionDespacho
from clases.vehiculo import (
    VehiculoCamion,
    VehiculoFurgoneta,
    VehiculoMotocicleta,
    VehiculoMochila
)


# ==========================================================
# CREAR VEHICULO
# ==========================================================

def crear_vehiculo(tipo, matricula, disponible=True):
    """
    Función factoría (factory) que crea un objeto Vehiculo
    en función del tipo recibido.

    Parámetros:
    - tipo: string que indica el tipo de vehículo
    - matricula: identificador del vehículo
    - disponible: estado del vehículo

    Devuelve:
    - objeto Vehiculo correspondiente
    """

    if tipo == "camion":
        return VehiculoCamion(matricula, disponible)

    elif tipo == "furgoneta":
        return VehiculoFurgoneta(matricula, disponible)

    elif tipo == "motocicleta":
        return VehiculoMotocicleta(matricula, disponible)

    elif tipo == "mochila":
        return VehiculoMochila(matricula, disponible)

    # Si no coincide ningún tipo
    return None



# ==========================================================
# GUARDAR DELEGACIONES
# ==========================================================

def guardar_delegaciones(delegaciones):
    """
    Guarda una lista de delegaciones en un fichero JSON.

    Convierte los objetos en estructuras de datos (diccionarios)
    que puedan ser serializadas en JSON.

    Parámetro:
    - delegaciones: lista de objetos Delegacion
    """

    # Obtener la ruta base del proyecto
    BASE_DIR = encontrar_raiz()

    if BASE_DIR is None:
        return

    # Ruta donde se guardará el fichero
    ruta = os.path.join(BASE_DIR, "datos", "delegaciones.json")

    # Lista donde almacenaremos los datos serializados
    data = []

    # Recorremos cada delegación
    for d in delegaciones:

        # Convertimos los vehículos en diccionarios
        vehiculos = []
        if d.flota:
            vehiculos = [
                {
                    "tipo": v.tipo,
                    "matricula": v.matricula,
                    "disponible": v.disponible
                }
                for v in d.flota.vehiculos
            ]

        # Convertimos la delegación a diccionario
        data.append({
            "tipo": d.__class__.__name__,   # Guardamos tipo de clase
            "nombre": d.nombre,
            "direccion": d.direccion,
            "coordenadas": d.coordenadas,
            "vehiculos": vehiculos
        })

    # Crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # Guardar fichero JSON
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print("Fichero guardado en:", ruta)


# ==========================================================
# CARGAR DELEGACIONES
# ==========================================================

def cargar_delegaciones():
    """
    Carga las delegaciones desde un fichero JSON y reconstruye
    los objetos originales (delegaciones y vehículos).

    Devuelve:
    - lista de objetos Delegacion
    """

    # Obtener ruta base del proyecto
    BASE_DIR = encontrar_raiz()

    if BASE_DIR is None:
        return []

    ruta = os.path.join(BASE_DIR, "datos", "delegaciones.json")

    # Comprobar si existe el fichero
    if not os.path.exists(ruta):
        print("No existe el fichero:", ruta)
        return []

    # Leer el fichero JSON
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    delegaciones = []

    # Reconstruir objetos
    for item in data:

        # Crear la delegación según su tipo
        if item["tipo"] == "DelegacionCentral":
            d = DelegacionCentral(item["nombre"], item["direccion"])
        else:
            d = DelegacionDespacho(item["nombre"], item["direccion"])

        # Restaurar coordenadas
        d._coordenadas = tuple(item["coordenadas"]) if item["coordenadas"] else None

        # Crear la flota de la delegación
        d.asignar_flota()

        # Reconstruir vehículos
        for v in item["vehiculos"]:
            vehiculo = crear_vehiculo(
                v["tipo"],
                v["matricula"],
                v["disponible"]
            )

            if vehiculo:
                d.flota.añadir_vehiculo(vehiculo)

        delegaciones.append(d)

    return delegaciones



