# ==========================================================
# DESCRIPCIÓN GENERAL DEL MÓDULO
# ==========================================================
"""
MÓDULO UTILS - SISTEMA LOGÍSTICO

Este módulo contiene funciones auxiliares utilizadas en todo el proyecto
de logística. Su objetivo es centralizar funcionalidades comunes para evitar
duplicación de código y mejorar la mantenibilidad.

FUNCIONALIDADES PRINCIPALES:

1. 🌍 Geocodificación de direcciones:
   - Uso de Nominatim (OpenStreetMap)
   - Sistema de cache en memoria + persistente (JSON)
   - Manejo de errores (timeout, rate limit)
   - Normalización de direcciones

2. 📏 Cálculo de distancias:
   - Implementación de fórmula de Haversine

3. 🚚 Gestión de vehículos:
   - Generación de matrículas aleatorias
   - Validación de matrículas españolas

4. 🗺️ Visualización:
   - Generación de mapas interactivos con Folium

5. 📁 Utilidades de sistema:
   - Detección automática de la raíz del proyecto

OBJETIVO:
Proveer herramientas reutilizables, eficientes y robustas para el sistema logístico.

NOTA:
Incluye optimizaciones clave como cache de geocodificación para evitar llamadas
repetidas a servicios externos (mejorando mucho el rendimiento).
"""

# ==========================================================
# IMPORTS
# ==========================================================

# Librerías para geocodificación
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderRateLimited

# Funciones matemáticas para cálculo de distancias
from math import radians, sin, cos, sqrt, atan2

# Otras utilidades
import random
import folium
import os
import sys
import subprocess
import time

# Añadir la raíz del proyecto al path para permitir imports relativos
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

# Import de persistencia de cache (JSON)
from persistencia.geocoding_cache import cargar_cache, guardar_cache


# ==========================================================
# CONFIGURACIÓN GEOCODER
# ==========================================================

# Instancia del geolocalizador (OpenStreetMap)
_geolocator = Nominatim(user_agent="logistica_app")


# ==========================================================
# GEOCODIFICACIÓN ROBUSTA
# ==========================================================

def geocodificar_direccion(txt):
    """
    Convierte una dirección en coordenadas (lat, lon).
    SOLO geocodifica (sin cache).
    El cache se gestiona fuera.
    """

    txt = normalizar_direccion(txt)

    try:
        time.sleep(1)

        location = _geolocator.geocode(txt, timeout=5)

        if location:
            return (location.latitude, location.longitude)

    except GeocoderRateLimited:
        print("⚠️ Rate limit, esperando...")
        time.sleep(3)
        return geocodificar_direccion(txt)

    except GeocoderTimedOut:
        pass

    # ------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------
    try:
        partes = txt.split(",")

        if len(partes) > 1:
            fallback = ",".join(partes[1:])

            time.sleep(1)

            location = _geolocator.geocode(fallback, timeout=5)

            if location:
                return (location.latitude, location.longitude)

    except:
        pass

    return None

# ==========================================================
# DISTANCIA HAVERSINE
# ==========================================================

def distancia_km(coord1, coord2):
    """
    Calcula la distancia entre dos coordenadas geográficas
    usando la fórmula de Haversine.

    Entrada:
        coord1 = (lat1, lon1)
        coord2 = (lat2, lon2)

    Salida:
        Distancia en kilómetros
    """

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371  # radio de la Tierra en km

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def generar_punto_cercano(lat, lon, radio_km=4):
    """
    Genera punto aleatorio en radio de X km
    """

    # convertir km a grados aprox
    radio_grados = radio_km / 111

    u = random.random()
    v = random.random()

    w = radio_grados * math.sqrt(u)
    t = 2 * math.pi * v

    delta_lat = w * math.cos(t)
    delta_lon = w * math.sin(t) / math.cos(math.radians(lat))

    return lat + delta_lat, lon + delta_lon


# ==========================================================
# MATRÍCULAS
# ==========================================================

def generar_matricula():
    """
    Genera una matrícula española aleatoria válida.
    Formato: 1234 ABC
    """

    numeros = random.randint(1000, 9999)

    letras = "BCDFGHJKLMNPRSTVWXYZ"
    sufijo = "".join(random.choice(letras) for _ in range(3))

    return f"{numeros} {sufijo}"


# ==========================================================
# VALIDAR MATRÍCULA ESPAÑOLA
# ==========================================================

def validar_matricula_esp(matricula):
    """
    Valida si una matrícula cumple el formato español moderno.
    """

    if not matricula:
        return False

    matricula = matricula.upper().replace(" ", "")

    if len(matricula) != 7:
        return False

    numeros = matricula[:4]
    letras = matricula[4:]

    if not numeros.isdigit():
        return False

    letras_validas = "BCDFGHJKLMNPRSTVWXYZ"

    for l in letras:
        if l not in letras_validas:
            return False

    return True


# ==========================================================
# ENCONTRAR RAÍZ DEL PROYECTO
# ==========================================================

def encontrar_raiz(proyecto="logistica"):
    """
    Busca la carpeta raíz del proyecto subiendo en el árbol de directorios.
    """

    ruta = os.path.abspath(os.path.dirname(__file__))

    while True:

        if os.path.basename(ruta) == proyecto:
            return ruta

        nueva = os.path.dirname(ruta)

        if nueva == ruta:
            return None

        ruta = nueva


# ==========================================================
# GENERAR MAPA (FOLIUM)
# ==========================================================

def generar_mapa(
        elementos,
        get_coord,
        get_popup,
        get_color=None,
        nombre_fichero="mapa.html",
        zoom=6,
        centro=(40, -3.7)
):
    """
    Genera un mapa interactivo con marcadores de las delegaciones.
    """

    print("\n🧭 Generando mapa...")

    mapa = folium.Map(location=centro, zoom_start=zoom)

    contador = 0

    for e in elementos:

        coord = get_coord(e)

        if not coord:
            print(f"⚠️ Sin coordenadas: {e}")
            continue

        lat, lon = coord

        if lat is None or lon is None:
            print(f"⚠️ Coordenadas inválidas: {e}")
            continue

        color = get_color(e) if get_color else "blue"

        folium.Marker(
            location=[lat, lon],
            popup=get_popup(e),
            icon=folium.Icon(color=color)
        ).add_to(mapa)

        contador += 1

    BASE_DIR = encontrar_raiz()

    if BASE_DIR is None:
        print("❌ No se pudo encontrar la raíz del proyecto")
        return

    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    mapa.save(ruta)

    print(f"✔ Mapa guardado en: {ruta}")
    print(f"✔ Elementos pintados: {contador}")

    try:
        subprocess.run(["open", ruta])
    except:
        print("⚠️ No se pudo abrir automáticamente el mapa")


# ==========================================================
# GEOLOCALIZACIÓN CON LOG
# ==========================================================

def geocodificar_con_log(direcciones):
    """
    Geocodifica direcciones SIN cache (solo diagnóstico).
    """

    coords = {}
    fallidas = []

    for d in direcciones:

        coord = geocodificar_direccion(d)

        if coord is None:
            fallidas.append(d)
        else:
            coords[d] = coord

    return coords, fallidas


# ==========================================================
# GEOLOCALIZACIÓN CON CACHE (MÚLTIPLE)
# ==========================================================
def geocodificar_con_cache(direccion):
    """
    Geocodificación unificada:
    - Cache en memoria (rápido)
    - Cache persistente (JSON)
    """

    cache = obtener_cache()

    direccion_norm = normalizar_direccion(direccion)

    # ------------------------------------------------------
    # CACHE
    # ------------------------------------------------------
    if direccion_norm in cache:
        print(f"♻️ Cache: {direccion}")
        return tuple(cache[direccion_norm])

    # ------------------------------------------------------
    # GEOLOCALIZACIÓN
    # ------------------------------------------------------
    print(f"🌐 Geocodificando: {direccion}")

    coord = geocodificar_direccion(direccion)

    if coord:
        cache[direccion_norm] = coord
        guardar_cache_global()

    return coord


# ==========================================================
# CACHE GLOBAL UNIFICADO
# ==========================================================

_cache_global = None


def obtener_cache():
    global _cache_global

    if _cache_global is None:
        _cache_global = cargar_cache()
        print(f"💾 Cache cargado: {len(_cache_global)} direcciones")

    return _cache_global


def guardar_cache_global():
    global _cache_global

    if _cache_global is not None:
        guardar_cache(_cache_global)


# ==========================================================
# NORMALIZAR DIRECCIÓN
# ==========================================================

def normalizar_direccion(txt):
    return " ".join(txt.strip().lower().split())


# ==========================================================
# GEOLOCALIZACIÓN PURA (SIN CACHE)
# ==========================================================

def geocodificar_direccion(txt):

    txt = normalizar_direccion(txt)

    try:
        time.sleep(1)

        location = _geolocator.geocode(txt, timeout=5)

        if location:
            return (location.latitude, location.longitude)

    except GeocoderRateLimited:
        print("⚠️ Rate limit, esperando...")
        time.sleep(3)
        return geocodificar_direccion(txt)

    except GeocoderTimedOut:
        pass

    # fallback
    try:
        partes = txt.split(",")

        if len(partes) > 1:
            fallback = ",".join(partes[1:])

            time.sleep(1)

            location = _geolocator.geocode(fallback, timeout=5)

            if location:
                return (location.latitude, location.longitude)

    except:
        pass

    return None


# ==========================================================
# GEOLOCALIZACIÓN CON CACHE (CORE)
# ==========================================================

_stats = {
    "cache": 0,
    "api": 0,
    "fallidas": 0
}


def geocodificar(direccion):
    """
    FUNCIÓN ÚNICA DEL SISTEMA
    """

    cache = obtener_cache()
    d_norm = normalizar_direccion(direccion)

    # CACHE
    if d_norm in cache:
        print(f"♻️ Cache: {direccion}")
        _stats["cache"] += 1
        return tuple(cache[d_norm])

    # API
    print(f"🌐 Geocodificando: {direccion}")
    _stats["api"] += 1

    coord = geocodificar_direccion(direccion)

    if coord:
        cache[d_norm] = coord
    else:
        _stats["fallidas"] += 1

    return coord


# ==========================================================
# GEOLOCALIZACIÓN LISTA
# ==========================================================

def geocodificar_lista(direcciones):

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
# GUARDADO FINAL + STATS
# ==========================================================

def cerrar_geocoding():
    """
    Guarda cache UNA SOLA VEZ + estadísticas
    """

    guardar_cache_global()

    print("\n📊 RESUMEN GEOLOCALIZACIÓN:")
    print(f"♻️ Cache usadas: {_stats['cache']}")
    print(f"🌐 Llamadas API: {_stats['api']}")
    print(f"❌ Fallidas: {_stats['fallidas']}")
    print(f"💾 Total cache: {len(obtener_cache())}\n")

