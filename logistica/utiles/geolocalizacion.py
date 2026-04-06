"""
==========================================================
UTILIDADES DE GEOLOCALIZACIÓN (AVANZADO)
==========================================================

- Geocodifica direcciones reales
- Cache persistente (JSON)
- Genera direcciones nuevas si faltan
==========================================================
"""

from geopy.geocoders import Nominatim
import time
import json
import os
import random

geolocator = Nominatim(user_agent="logistica_app")

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "datos", "cache_direcciones.json")

# -----------------------------------------
# CARGAR CACHE
# -----------------------------------------
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        CACHE = json.load(f)
else:
    CACHE = {}


# -----------------------------------------
# GUARDAR CACHE
# -----------------------------------------
def guardar_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f, indent=4)


# -----------------------------------------
# GEOLOCALIZAR
# -----------------------------------------
def geolocalizar_direccion(direccion):

    if direccion in CACHE:
        return tuple(CACHE[direccion])

    try:
        loc = geolocator.geocode(direccion)

        if loc:
            coord = (loc.latitude, loc.longitude)
            CACHE[direccion] = coord
            guardar_cache()
            time.sleep(1)
            return coord

    except:
        pass

    return None


# -----------------------------------------
# GENERAR DIRECCION DINAMICA
# -----------------------------------------
def generar_direccion_dinamica(ciudad):

    for _ in range(5):

        try:
            numero = random.randint(1, 200)
            query = f"calle {numero}, {ciudad}, España"

            loc = geolocator.geocode(query)

            if loc:
                direccion = loc.address
                coord = (loc.latitude, loc.longitude)

                if direccion not in CACHE:
                    CACHE[direccion] = coord
                    guardar_cache()

                return direccion, coord

            time.sleep(1)

        except:
            continue

    return None, None

def direccion_cercana(coord):
    """
    Busca una dirección real cercana a unas coordenadas
    usando reverse geocoding
    """

    lat, lon = coord

    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location:
            return location.address

    except:
        pass

    return None