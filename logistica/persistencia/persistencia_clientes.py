"""
MODULO PERSISTENCIA CLIENTES

Este modulo se encarga de la persistencia de los clientes del sistema.
Permite guardar y recuperar la informacion de los clientes utilizando
un fichero en formato JSON.

FUNCIONALIDAD DEL MODULO

1. guardar_clientes(clientes)
   - Recibe un diccionario de objetos Cliente
   - Convierte los objetos en estructuras de datos simples
   - Guarda la informacion en un fichero JSON
   - Almacena datos personales, direccion, pedidos e importe facturado

2. cargar_clientes()
   - Lee el fichero JSON de clientes
   - Reconstruye los objetos Cliente y Direccion
   - Restaura listas de pedidos e importe facturado
   - Devuelve un diccionario de clientes listo para usar

IDEA PRINCIPAL

El formato JSON no permite guardar objetos directamente,
por lo que es necesario:

- SERIALIZAR (guardar):
  convertir objetos a datos simples (diccionarios, listas, numeros)

- DESERIALIZAR (cargar):
  reconstruir los objetos a partir de esos datos

ESTRUCTURA DEL JSON

clientes = {
    dni: {
        nombre,
        apellidos,
        direccion: {
            pais, provincia, ciudad, calle, numero, coordenadas
        },
        pedidos_en_curso,
        pedidos_terminados,
        importe_facturado
    }
}
"""


import json
import os
from clases.cliente import Cliente
from clases.direccion import Direccion
import utiles.utils as utils


# ==========================================
# GUARDAR CLIENTES
# ==========================================
def guardar_clientes(clientes):

    """
    FUNCION guardar_clientes

    OBJETIVO
    Guardar en un fichero JSON todos los clientes del sistema

    PARAMETROS
    clientes: diccionario {dni: objeto Cliente}

    FUNCIONAMIENTO

    1. Obtiene la ruta base del proyecto
    2. Construye la ruta del fichero JSON
    3. Recorre todos los clientes
    4. Convierte cada objeto en un diccionario
    5. Guarda el resultado en formato JSON

    RESULTADO
    Se crea o actualiza el fichero clientes.json
    """

    # obtener ruta base del proyecto
    BASE_DIR = utils.encontrar_raiz()

    # construir ruta al fichero json
    ruta = os.path.join(BASE_DIR, "datos", "clientes.json")

    # diccionario donde se almacenaran los datos serializados
    data = {}

    # recorrer todos los clientes
    for dni, c in clientes.items():

        # obtener direccion del cliente
        d = c._direccion

        # construir estructura de datos para json
        data[dni] = {

            # datos personales
            "nombre": c._nombre,
            "apellidos": c._apellidos,

            # direccion descompuesta
            "direccion": {
                "pais": d._pais,
                "provincia": d._provincia,
                "ciudad": d._ciudad,
                "calle": d._calle,
                "numero": d._numero,
                "coordenadas": d.coordenadas
            },

            # listas de pedidos
            "pedidos_en_curso": [p for p in c._pedidos_en_curso],
            "pedidos_terminados": [p for p in c._pedidos_terminados],

            # importe total
            "importe_facturado": c._importe_facturado
        }

    # crear carpeta si no existe
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    # guardar fichero json
    with open(ruta, "w", encoding="utf-8") as f:

        # indent mejora la lectura
        # ensure_ascii permite guardar caracteres especiales
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Clientes guardados en JSON")


# ==========================================
# CARGAR CLIENTES
# ==========================================
def cargar_clientes():

    """
    FUNCION cargar_clientes

    OBJETIVO
    Cargar los clientes desde un fichero JSON

    FUNCIONAMIENTO

    1. Obtiene la ruta base del proyecto
    2. Comprueba si el fichero existe
    3. Lee el contenido JSON
    4. Recorre los datos
    5. Reconstruye objetos Direccion
    6. Reconstruye objetos Cliente
    7. Restaura atributos adicionales

    RESULTADO
    Devuelve un diccionario {dni: objeto Cliente}
    """

    # obtener ruta base
    BASE_DIR = utils.encontrar_raiz()

    # ruta del fichero
    ruta = os.path.join(BASE_DIR, "datos", "clientes.json")

    # si no existe, devolver vacio
    if not os.path.exists(ruta):
        return {}

    # leer fichero json
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    # diccionario de clientes reconstruidos
    clientes = {}

    # recorrer datos
    for dni, info in data.items():

        # obtener direccion
        d = info["direccion"]

        # reconstruir objeto Direccion
        direccion = Direccion(
            pais=d["pais"],
            provincia=d["provincia"],
            ciudad=d["ciudad"],
            calle=d["calle"],
            numero=d["numero"]
        )

        # restaurar coordenadas
        direccion.coordenadas = tuple(d["coordenadas"]) if d["coordenadas"] else None

        # reconstruir cliente
        c = Cliente(
            dni=dni,
            nombre=info["nombre"],
            apellidos=info["apellidos"],
            direccion=direccion
        )

        # restaurar listas de pedidos
        c._pedidos_en_curso = info.get("pedidos_en_curso", [])
        c._pedidos_terminados = info.get("pedidos_terminados", [])

        # restaurar importe
        c._importe_facturado = info.get("importe_facturado", 0)

        # añadir al diccionario
        clientes[dni] = c

    return clientes