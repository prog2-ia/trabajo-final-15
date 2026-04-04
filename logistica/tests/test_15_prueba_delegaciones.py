# ==========================================================
# DESCRIPCIÓN GENERAL DEL PROGRAMA
# ==========================================================
"""
SCRIPT DE TESTING: RED DE DELEGACIONES LOGÍSTICAS

Este programa construye y valida una red logística completa formada por:

- 1 Delegación Central
- Varias Delegaciones Base
- Múltiples Delegaciones de Despacho

FUNCIONALIDADES PRINCIPALES:

1. Creación de la estructura jerárquica de delegaciones
2. Generación automática de flotas de vehículos
3. Geocodificación de direcciones (obtención de coordenadas)
4. Asignación de cada despacho a la base más cercana (criterio geográfico)
5. Detección de direcciones no geolocalizadas
6. Persistencia de datos en fichero (JSON)
7. Verificación de coordenadas tras carga
8. Visualización:
   - Árbol jerárquico de la red
   - Mapa interactivo HTML con todas las delegaciones

OBJETIVO:
Validar que todo el sistema (clases, utilidades, persistencia y geolocalización)
funciona correctamente de forma integrada.

NOTA:
El script está preparado para ejecutarse desde cualquier ruta gracias a la
modificación dinámica del sys.path.
"""

# ==========================================================
# IMPORTS
# ==========================================================

import sys
import os

# Añadir la raíz del proyecto al path para permitir imports relativos
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

# Clases de delegaciones
from clases.delegacion import (
    DelegacionCentral,
    DelegacionBase,
    DelegacionDespacho
)

# Clases de vehículos
from clases.vehiculo import (
    VehiculoCamion,
    VehiculoFurgoneta
)

# Funciones de persistencia (guardar/cargar JSON)
from persistencia.persistencia_delegaciones import (
    guardar_delegaciones,
    cargar_delegaciones
)

# Utilidades varias
from utiles.utils import (
    generar_matricula,
    distancia_km,
    geocodificar_direccion,
    generar_mapa,
    geocodificar_con_log,
    geocodificar_con_cache,
    geocodificar_lista
)

# Datos externos (direcciones ya limpias y normalizadas)
from datos.direcciones import (
    direcciones_central_txt,
    direcciones_base_txt,
    direcciones_despacho_txt
)


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================

def poblar_flota(d):
    """
    Añade vehículos a la flota de una delegación.

    - Si es central → añade camiones
    - Si es base o despacho → añade furgonetas

    Cada delegación recibe 2 vehículos.
    """
    if isinstance(d, DelegacionCentral):
        for _ in range(2):
            d.flota.añadir_vehiculo(VehiculoCamion(generar_matricula()))
    else:
        for _ in range(2):
            d.flota.añadir_vehiculo(VehiculoFurgoneta(generar_matricula()))


def asignar_base(coord, bases):
    """
    Devuelve la delegación base más cercana a unas coordenadas dadas.

    Utiliza:
    - distancia_km() para calcular distancias
    - min() con función lambda como criterio

    Implementa una lógica tipo "vecino más cercano".
    """
    return min(
        bases,
        key=lambda b: distancia_km(coord, b.coordenadas)
    )


def imprimir_arbol(delegaciones):
    """
    Imprime la estructura jerárquica de la red logística en consola:

    Central
      ├── Base
      │     ├── Despacho
    """

    print("\n========== RED LOGÍSTICA ==========\n")

    # Obtener la central
    central = next(d for d in delegaciones if isinstance(d, DelegacionCentral))
    print(f"{central.nombre} ({central.direccion})")

    # Obtener todas las bases
    bases = [d for d in delegaciones if isinstance(d, DelegacionBase)]

    for b in bases:
        print(f"   ├── {b.nombre} ({b.direccion})")

        # Filtrar despachos asociados a esa base
        despachos = [
            d for d in delegaciones
            if isinstance(d, DelegacionDespacho) and d.delegacion_superior == b
        ]

        for d in despachos:
            print(f"   │     ├── {d.nombre} ({d.direccion})")


def get_coord(d):
    """Devuelve las coordenadas de una delegación (para el mapa)."""
    return d.coordenadas


def get_popup(d):
    """Texto HTML que aparece al hacer click en el marcador del mapa."""
    return f"{d.nombre}<br>{d.direccion}"


def get_color(d):
    """
    Define el color del marcador según el tipo de delegación:

    - Central → rojo
    - Base → azul
    - Despacho → verde
    """
    if isinstance(d, DelegacionCentral):
        return "red"
    elif isinstance(d, DelegacionBase):
        return "blue"
    else:
        return "green"


# ==========================================================
# MAIN
# ==========================================================

print("\n🚀 Iniciando test de delegaciones...\n")

# ----------------------------------------------------------
# CREACIÓN DE LA DELEGACIÓN CENTRAL
# ----------------------------------------------------------

central = DelegacionCentral("Central Madrid", direcciones_central_txt[0])

central.asignar_flota()   # Inicializa la flota
poblar_flota(central)     # Añade vehículos

# Calcular coordenadas SOLO UNA VEZ (optimización)
central.calcular_coordenadas()


# ----------------------------------------------------------
# CREACIÓN DE DELEGACIONES BASE
# ----------------------------------------------------------

bases = []

for i, txt in enumerate(direcciones_base_txt):

    # Crear base asociada a la central
    b = DelegacionBase(f"Base {i+1}", txt, central)

    b.asignar_flota()
    poblar_flota(b)

    # Calcular coordenadas de la base
    b.calcular_coordenadas()

    bases.append(b)


# ----------------------------------------------------------
# CREACIÓN DE DESPACHOS (CON GEOLOG Y CONTROL DE ERRORES)
# ----------------------------------------------------------

# Geocodificación masiva con control de fallos
coords_despachos, fallidas = geocodificar_lista(direcciones_despacho_txt)

despachos = []

for i, (txt, coord) in enumerate(coords_despachos.items()):

    # Asignar despacho a la base más cercana
    base = asignar_base(coord, bases)

    d = DelegacionDespacho(f"Despacho {i+1}", txt, base)

    d.asignar_flota()
    poblar_flota(d)

    # Asignar coordenadas directamente (evita recalcular)
    d._coordenadas = coord

    despachos.append(d)


# ----------------------------------------------------------
# INFORME DE GEOLOCALIZACIÓN
# ----------------------------------------------------------

print("\n🔎 INFORME DE GEOLOCALIZACIÓN\n")

print(f"✔ Direcciones válidas: {len(coords_despachos)}")
print(f"❌ Direcciones fallidas: {len(fallidas)}\n")

if fallidas:
    print("⚠️ LISTADO DE DIRECCIONES NO GEOLOCALIZADAS:\n")
    for d in fallidas:
        print(" -", d)


# ==========================================================
# PERSISTENCIA
# ==========================================================

# Agrupar todas las delegaciones
todas = [central] + bases + despachos

# Guardar en fichero JSON
guardar_delegaciones(todas)

# Cargar desde fichero para comprobar integridad
delegaciones = cargar_delegaciones()

# Verificar estado de coordenadas
print("\n🔎 ESTADO DE GEOLOCALIZACIÓN:\n")

for d in delegaciones:
    if hasattr(d, "coordenadas") and d.coordenadas:
        print(f"{d.nombre} -> 🌍 {d.coordenadas}")
    else:
        print(f"{d.nombre} -> 📍 {d.direccion} (SIN GEO)")


# ==========================================================
# SALIDA POR CONSOLA
# ==========================================================

# Mostrar estructura jerárquica
imprimir_arbol(delegaciones)


# ==========================================================
# GENERACIÓN DE MAPA
# ==========================================================

# Genera un mapa HTML interactivo con todas las delegaciones
generar_mapa(
    delegaciones,
    get_coord,
    get_popup,
    get_color,
    nombre_fichero="mapa_delegaciones.html"
)