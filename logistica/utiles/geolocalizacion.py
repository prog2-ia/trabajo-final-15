# ==========================================================
# GEOLOCALIZACIÓN CENTRALIZADA (VERSIÓN LIMPIA)
# ==========================================================

import json
import os
import time

from geopy.exc import GeocoderTimedOut, GeocoderRateLimited
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="logistica_app")

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "datos", "cache_direcciones.json")

# ==========================================================
# CACHE
# ==========================================================
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        CACHE = json.load(f)
else:
    CACHE = {}


def guardar_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f, indent=4)


# ==========================================================
# NORMALIZAR
# ==========================================================
def normalizar_direccion(txt):
    return " ".join(txt.strip().lower().split())


# ==========================================================
# GEOLOCALIZAR (CON CACHE)
# ==========================================================
def geocodificar(direccion):
    direccion_norm = normalizar_direccion(direccion)

    if direccion_norm in CACHE:
        print(f"♻️ Cache: {direccion}")
        return tuple(CACHE[direccion_norm])

    print(f"🌐 Geocodificando: {direccion}")

    try:
        time.sleep(1)

        loc = geolocator.geocode(direccion_norm, timeout=5)

        if loc:
            coord = (loc.latitude, loc.longitude)
            CACHE[direccion_norm] = coord
            guardar_cache()
            return coord

    except GeocoderRateLimited:
        time.sleep(3)
        return geocodificar(direccion)

    except GeocoderTimedOut:
        pass

    # fallback
    try:
        partes = direccion_norm.split(",")

        if len(partes) > 1:
            fallback = ",".join(partes[1:])
            loc = geolocator.geocode(fallback, timeout=5)

            if loc:
                coord = (loc.latitude, loc.longitude)
                CACHE[direccion_norm] = coord
                guardar_cache()
                return coord

    except:
        pass

    return None

# ==========================================================
# GEOLOCALIZACIÓN LISTA (VERSIÓN CORRECTA)
# ==========================================================
def geocodificar_lista(direcciones):
    """
    Geocodifica una lista de direcciones usando la función principal
    del sistema (geocodificar con cache).

    Devuelve:
        coords -> dict {direccion: (lat, lon)}
        fallidas -> lista de direcciones no geocodificadas
    """

    coords = {}
    fallidas = []

    for d in direcciones:

        # 🔥 USAR TU FUNCIÓN NUEVA
        coord = geocodificar(d)

        if coord is None:
            fallidas.append(d)
        else:
            coords[d] = coord

    return coords, fallidas
# ==========================================================
# REVERSE GEO
# ==========================================================
def direccion_cercana(coord):
    lat, lon = coord

    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location:
            return location.address

    except:
        pass

    return None
