# ==========================================================
# GEOLOCALIZACIÓN CENTRALIZADA
# ==========================================================
# Funcionalidades:
# - Geocodificación dirección -> coordenadas
# - Reverse geocoding coordenadas -> población/provincia
# - Cache persistente JSON
# - Cache en memoria
# - Reintentos automáticos
# - Protección contra rate-limit
# - Timeouts robustos
# ==========================================================

import json
import os
import time

from typing import Optional

from geopy.exc import (
    GeocoderTimedOut,
    GeocoderRateLimited
)  # type: ignore[import-untyped]

from geopy.geocoders import (
    Nominatim
)  # type: ignore[import-untyped]


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

geolocator = Nominatim(
    user_agent="logistica_app"
)

TIMEOUT = 10
REINTENTOS = 3
ESPERA_REINTENTO = 2
ESPERA_PETICION = 1


# ==========================================================
# CACHE FILE
# ==========================================================

CACHE_FILE = os.path.join(
    os.path.dirname(__file__),
    "..",
    "datos",
    "cache_direcciones.json"
)


# ==========================================================
# CARGA CACHE PERSISTENTE
# ==========================================================

if os.path.exists(CACHE_FILE):

    with open(CACHE_FILE, "r", encoding="utf-8") as f:

        CACHE = json.load(f)

else:

    CACHE = dict()


# ==========================================================
# CACHE GEO EN MEMORIA
# ==========================================================

CACHE_DATOS_GEO: dict[
    tuple[float, float],
    tuple[Optional[str], Optional[str]]
] = {}


# ==========================================================
# GUARDAR CACHE
# ==========================================================

def guardar_cache():

    os.makedirs(
        os.path.dirname(CACHE_FILE),
        exist_ok=True
    )

    with open(CACHE_FILE, "w", encoding="utf-8") as f:

        json.dump(
            CACHE,
            f,
            indent=4,
            ensure_ascii=False
        )


# ==========================================================
# NORMALIZAR DIRECCIÓN
# ==========================================================

def normalizar_direccion(txt):

    return " ".join(
        txt.strip().lower().split()
    )


# ==========================================================
# GEO → COORDENADAS
# ==========================================================

def geocodificar(direccion):

    if not direccion:
        return None

    direccion_norm = normalizar_direccion(direccion)

    # ------------------------------------------------------
    # CACHE
    # ------------------------------------------------------

    if direccion_norm in CACHE:

        print(f"♻️ Cache: {direccion}")

        return tuple(CACHE[direccion_norm])

    print(f"🌐 Geocodificando: {direccion}")

    # ------------------------------------------------------
    # REINTENTOS
    # ------------------------------------------------------

    for intento in range(REINTENTOS):

        try:

            time.sleep(ESPERA_PETICION)

            loc = geolocator.geocode(
                direccion_norm,
                timeout=TIMEOUT
            )

            if loc:

                coord = (
                    loc.latitude,
                    loc.longitude
                )

                CACHE[direccion_norm] = coord

                guardar_cache()

                return coord

            break

        except GeocoderRateLimited:

            print(
                f"⚠️ Rate limit "
                f"(intento {intento + 1})"
            )

            time.sleep(5)

        except GeocoderTimedOut:

            print(
                f"⚠️ Timeout GEO "
                f"(intento {intento + 1})"
            )

            time.sleep(ESPERA_REINTENTO)

        except Exception as e:

            print(f"⚠️ Error geocode: {e}")

            time.sleep(ESPERA_REINTENTO)

    # ------------------------------------------------------
    # FALLBACK SIN CALLE
    # ------------------------------------------------------

    try:

        partes = direccion_norm.split(",")

        if len(partes) > 1:

            fallback = ",".join(partes[1:])

            print(f"🔄 Fallback: {fallback}")

            for intento in range(REINTENTOS):

                try:

                    time.sleep(ESPERA_PETICION)

                    loc = geolocator.geocode(
                        fallback,
                        timeout=TIMEOUT
                    )

                    if loc:

                        coord = (
                            loc.latitude,
                            loc.longitude
                        )

                        CACHE[direccion_norm] = coord

                        guardar_cache()

                        return coord

                    break

                except Exception:

                    time.sleep(ESPERA_REINTENTO)

    except Exception:

        pass

    return None


# ==========================================================
# GEOLOCALIZAR LISTA
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

    # ------------------------------------------------------
    # CACHE MEMORIA
    # ------------------------------------------------------

    if coord in CACHE_DATOS_GEO:

        return CACHE_DATOS_GEO[coord]

    lat, lon = coord

    # ------------------------------------------------------
    # REINTENTOS
    # ------------------------------------------------------

    for intento in range(REINTENTOS):

        try:

            time.sleep(ESPERA_PETICION)

            location = geolocator.reverse(
                (lat, lon),
                exactly_one=True,
                timeout=TIMEOUT
            )

            if location and "address" in location.raw:

                addr = location.raw["address"]

                # ==================================================
                # POBLACIÓN
                # ==================================================

                poblacion = (

                    addr.get("city")

                    or addr.get("town")

                    or addr.get("village")

                    or addr.get("municipality")
                )

                # fallback urbano

                if not poblacion:

                    poblacion = (

                        addr.get("city_district")

                        or addr.get("suburb")

                        or addr.get("neighbourhood")
                    )

                # fallback usando address completo

                if not poblacion and location.address:

                    partes = location.address.split(",")

                    if len(partes) >= 4:

                        poblacion = partes[-4].strip()

                # limpieza "Elx / Elche"

                if poblacion and "/" in poblacion:

                    poblacion = (
                        poblacion.split("/")[-1].strip()
                    )

                # ==================================================
                # PROVINCIA
                # ==================================================

                provincia = (

                    addr.get("province")

                    or addr.get("state_district")

                    or addr.get("county")

                    or addr.get("state")
                )

                if provincia:

                    provincia = provincia.strip()

                    if "/" in provincia:

                        partes = [

                            p.strip()

                            for p in provincia.split("/")

                            if p.strip()
                        ]

                        provincia = (
                            partes[-1]
                            if partes
                            else provincia
                        )

                    # normalización Madrid

                    if "Madrid" in provincia:

                        provincia = "Madrid"

                resultado = (
                    poblacion,
                    provincia
                )

                # --------------------------------------------------
                # CACHE MEMORIA
                # --------------------------------------------------

                CACHE_DATOS_GEO[coord] = resultado

                print(
                    f"🌍 GEO OK: "
                    f"{poblacion} | {provincia}"
                )

                return resultado

            break

        except GeocoderRateLimited:

            print(
                f"⚠️ Rate limit reverse GEO "
                f"(intento {intento + 1})"
            )

            time.sleep(5)

        except GeocoderTimedOut:

            print(
                f"⚠️ Timeout reverse GEO "
                f"(intento {intento + 1})"
            )

            time.sleep(ESPERA_REINTENTO)

        except Exception as e:

            print(
                f"⚠️ Error reverse geo: "
                f"{coord} -> {e}"
            )

            time.sleep(ESPERA_REINTENTO)

    return None, None


# ==========================================================
# REVERSE GEO → DIRECCIÓN
# ==========================================================

def direccion_cercana(coord):

    if not coord:
        return None

    lat, lon = coord

    # ------------------------------------------------------
    # REINTENTOS
    # ------------------------------------------------------

    for intento in range(REINTENTOS):

        try:

            time.sleep(ESPERA_PETICION)

            location = geolocator.reverse(
                (lat, lon),
                exactly_one=True,
                timeout=TIMEOUT
            )

            if location:

                return location.address

            break

        except GeocoderRateLimited:

            print(
                f"⚠️ Rate limit dirección "
                f"(intento {intento + 1})"
            )

            time.sleep(5)

        except GeocoderTimedOut:

            print(
                f"⚠️ Timeout dirección "
                f"(intento {intento + 1})"
            )

            time.sleep(ESPERA_REINTENTO)

        except Exception as e:

            print(
                f"⚠️ Error dirección: "
                f"{coord} -> {e}"
            )

            time.sleep(ESPERA_REINTENTO)

    return None