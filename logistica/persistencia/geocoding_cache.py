# ==========================================================
# CACHE DE GEOLOCALIZACIÓN (PERSISTENTE)
# ==========================================================

import json
import os

# Ruta robusta (independiente del working directory)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
RUTA_CACHE = os.path.join(BASE_DIR, "datos", "geocoding_cache.json")


def cargar_cache():
    """
    Carga el cache desde JSON.
    Si no existe, devuelve diccionario vacío.
    """
    if not os.path.exists(RUTA_CACHE):
        return {}

    with open(RUTA_CACHE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_cache(cache):
    """
    Guarda el cache en JSON asegurando que la carpeta existe.
    """
    carpeta = os.path.dirname(RUTA_CACHE)
    os.makedirs(carpeta, exist_ok=True)

    with open(RUTA_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=4)