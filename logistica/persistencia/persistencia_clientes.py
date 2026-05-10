"""
==========================================================
MÓDULO: persistencia_clientes.py
==========================================================

Este módulo gestiona la persistencia de los clientes del sistema
logístico mediante ficheros JSON.

RESPONSABILIDADES:
✔ Guardar clientes en disco (serialización)
✔ Cargar clientes desde JSON (deserialización)
✔ Mantener coherencia con delegaciones
✔ Restaurar estado logístico completo del cliente
✔ Soportar evolución del formato de datos

CARACTERÍSTICAS CLAVE:
✔ Persistencia incremental o completa (sobrescribir=True)
✔ Compatibilidad con formatos antiguos (lista → dict)
✔ Normalización de nombres de delegaciones
✔ Restauración de relaciones (cliente → delegación)
✔ Persistencia de pedidos y facturación

ESTRUCTURA DEL JSON:
{
    "dni": {
        "nombre": str,
        "apellidos": str,
        "direccion": str,
        "coordenadas": [lat, lon],
        "delegacion_cercana": str,
        "provincia": str,
        "poblacion": str,
        "pedidos_en_curso": [ids],
        "pedidos_terminados": [ids],
        "importe_facturado": float,
        "distancia_despacho": float
    }
}

NOTAS IMPORTANTES:
✔ Se usa DNI como clave única
✔ Delegación se guarda como nombre (no objeto)
✔ Se reconstruye posteriormente mediante mapa
✔ Se evita duplicar objetos complejos en JSON
"""

# ==========================================================
# IMPORTS
# ==========================================================
import json
import os

from clases.cliente import Cliente
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.utils import encontrar_raiz


# ==========================================================
# NORMALIZACIÓN DE TEXTO
# ==========================================================
def normalizar(texto):
    """
    Normaliza texto para comparaciones consistentes.

    ✔ Elimina espacios
    ✔ Convierte a minúsculas
    ✔ Evita errores en matching de nombres

    Uso clave:
    - Comparar nombres de delegaciones
    """
    return (texto or "").strip().lower()


# ==========================================================
# GUARDAR CLIENTES
# ==========================================================
def guardar_clientes(clientes_nuevos, sobrescribir=False):
    """
    Guarda clientes en fichero JSON.

    MODOS:
    ✔ sobrescribir=True  → reemplaza todo el fichero
    ✔ sobrescribir=False → añade/actualiza registros

    Parámetros:
    - clientes_nuevos: dict {dni: Cliente}
    - sobrescribir: bool
    """

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", "clientes.json")

    # ------------------------------------------------------
    # CARGA INICIAL (SEGÚN MODO)
    # ------------------------------------------------------
    if sobrescribir:
        data = {}
    else:
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}

        # --------------------------------------------------
        # COMPATIBILIDAD CON FORMATO ANTIGUO
        # --------------------------------------------------
        # Convierte lista → dict indexado por DNI
        if isinstance(data, list):
            data = {item["dni"]: item for item in data if "dni" in item}

    # ------------------------------------------------------
    # SERIALIZACIÓN DE CLIENTES
    # ------------------------------------------------------
    for dni, c in clientes_nuevos.items():

        data[dni] = {
            "nombre": c._nombre,
            "apellidos": c._apellidos,
            "direccion": c._direccion,
            "coordenadas": c._coordenadas,

            # Delegación se guarda como nombre normalizado
            "delegacion_cercana": (
                normalizar(c._delegacion_cercana.nombre)
                if c._delegacion_cercana else None
            ),

            # Datos geográficos
            "provincia": getattr(c, "_provincia", None),
            "poblacion": getattr(c, "_poblacion", None),

            # Datos logísticos
            "pedidos_en_curso": c._pedidos_en_curso,
            "pedidos_terminados": c._pedidos_terminados,
            "importe_facturado": c._importe_facturado,
            "distancia_despacho": c._distancia_despacho
        }

    # ------------------------------------------------------
    # ESCRITURA EN FICHERO
    # ------------------------------------------------------
    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✔ Clientes guardados: {len(data)}")


# ==========================================================
# CARGAR CLIENTES
# ==========================================================
def cargar_clientes(nombre_fichero="clientes.json"):
    """
    Carga clientes desde JSON y reconstruye objetos Cliente.

    ✔ Restaura datos personales
    ✔ Restaura datos geográficos
    ✔ Restaura pedidos y facturación
    ✔ Reconstruye relación con delegaciones

    Retorna:
    - dict {dni: Cliente}
    """

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    if not os.path.exists(ruta):
        return {}

    # ------------------------------------------------------
    # LECTURA JSON
    # ------------------------------------------------------
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ------------------------------------------------------
    # CARGAR DELEGACIONES
    # ------------------------------------------------------
    delegaciones = cargar_delegaciones()

    # ------------------------------------------------------
    # MAPA NORMALIZADO (CLAVE)
    # ------------------------------------------------------
    # Permite reconstruir relación cliente → delegación
    mapa = {normalizar(d.nombre): d for d in delegaciones}

    clientes = {}

    # ------------------------------------------------------
    # COMPATIBILIDAD DE FORMATOS
    # ------------------------------------------------------
    if isinstance(data, dict):
        iterable = data.items()
    else:
        iterable = [(item.get("dni"), item) for item in data]

    # ------------------------------------------------------
    # DESERIALIZACIÓN
    # ------------------------------------------------------
    for dni, item in iterable:

        if not dni:
            continue

        # --------------------------------------------------
        # RECONSTRUIR DELEGACIÓN
        # --------------------------------------------------
        nombre_deleg = normalizar(item.get("delegacion_cercana"))
        deleg = mapa.get(nombre_deleg)

        # --------------------------------------------------
        # CREAR OBJETO CLIENTE
        # --------------------------------------------------
        c = Cliente(
            dni,
            item.get("nombre"),
            item.get("apellidos"),
            item.get("direccion"),
            deleg
        )

        # --------------------------------------------------
        # RESTAURAR DATOS
        # --------------------------------------------------
        coords = item.get("coordenadas")
        c._coordenadas = tuple(coords) if coords else None

        c._poblacion = item.get("poblacion")
        c._provincia = item.get("provincia")

        c._pedidos_en_curso = item.get("pedidos_en_curso", [])
        c._pedidos_terminados = item.get("pedidos_terminados", [])
        c._importe_facturado = item.get("importe_facturado", 0)

        c._delegacion_cercana = deleg
        c._distancia_despacho = item.get("distancia_despacho")

        clientes[dni] = c

    print(f"✔ Clientes cargados: {len(clientes)}")

    return clientes