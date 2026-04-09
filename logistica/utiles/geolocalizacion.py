# ==========================================================
# GEOLOCALIZACIÓN CENTRALIZADA (VERSIÓN FINAL)
# ==========================================================

import json
import os
import time

from geopy.exc import GeocoderTimedOut, GeocoderRateLimited
from geopy.geocoders import Nominatim

# ==========================================================
# CONFIG
# ==========================================================
geolocator = Nominatim(user_agent="logistica_app")

CACHE_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "datos",
    "cache_direcciones.json"
)

# ==========================================================
# CACHE COORDENADAS
# ==========================================================
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        CACHE = json.load(f)
else:
    CACHE = {}

CACHE_DATOS_GEO = {}


def guardar_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(CACHE, f, indent=4)


# ==========================================================
# NORMALIZAR
# ==========================================================
def normalizar_direccion(txt):
    return " ".join(txt.strip().lower().split())


# ==========================================================
# GEO → COORDENADAS
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
        print("⚠️ Rate limit, esperando...")
        time.sleep(3)
        return geocodificar(direccion)

    except GeocoderTimedOut:
        pass

    # fallback sin calle
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
# GEOLOCALIZAR LISTA (RESTAURADA)
# ==========================================================
def geocodificar_lista(direcciones):
    """
    Devuelve:
        dict {direccion: coordenadas}
        lista de direcciones fallidas
    """

    coords = {}
    fallidas = []

    for d in direcciones:

        coord = geocodificar(d)

        if coord is None:
            fallidas.append(d)
        else:
            coords[d] = coord

    return coords, fallidas
# ==========================================================
# REVERSE GEO → DATOS
# ==========================================================
def obtener_datos_geo(coord):

    if not coord:
        return None, None

    if coord in CACHE_DATOS_GEO:
        return CACHE_DATOS_GEO[coord]

    lat, lon = coord

    try:
        time.sleep(1)

        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location and "address" in location.raw:

            addr = location.raw["address"]

            # -----------------------------
            # POBLACIÓN
            # -----------------------------
            # --------------------------------------------------
            # POBLACIÓN (VERSIÓN DEFINITIVA ESPAÑA)
            # --------------------------------------------------
            poblacion = (
                    addr.get("city")  # Madrid, Elche
                    or addr.get("town")  # pueblos
                    or addr.get("village")
                    or addr.get("municipality")
            )

            # 🔥 fallback urbano (MUY IMPORTANTE en Madrid)
            if not poblacion:
                poblacion = (
                        addr.get("city_district")  # Villaverde
                        or addr.get("suburb")  # barrios
                        or addr.get("neighbourhood")
                )

            # 🔥 fallback final usando texto completo
            if not poblacion and location.address:
                partes = location.address.split(",")
                if len(partes) >= 3:
                    poblacion = partes[-4].strip()  # suele ser ciudad real


            # limpiar tipo "Elx / Elche"
            if poblacion and "/" in poblacion:
                poblacion = poblacion.split("/")[-1].strip()

            # -----------------------------
            # PROVINCIA
            # -----------------------------
            provincia = (
                    addr.get("province")
                    or addr.get("state_district")
                    or addr.get("county")
                    or addr.get("state")
            )
            # provincia = addr.get("province")

            if provincia:
                provincia = provincia.strip()

                if "/" in provincia:
                    partes = [p.strip() for p in provincia.split("/") if p.strip()]
                    provincia = partes[-1] if partes else provincia

                # 🔥 normalización Madrid
                if "Madrid" in provincia:
                    provincia = "Madrid"

            resultado = (poblacion, provincia)

            CACHE_DATOS_GEO[coord] = resultado

            # print(f"🌍 GEO OK: {poblacion} | {provincia}")

            return resultado

    except Exception as e:
        print(f"⚠️ Error reverse geo: {coord} -> {e}")

    return None, None


# ==========================================================
# REVERSE GEO → DIRECCIÓN
# ==========================================================
def direccion_cercana(coord):

    if not coord:
        return None

    lat, lon = coord

    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)

        if location:
            return location.address

    except:
        pass

    return None