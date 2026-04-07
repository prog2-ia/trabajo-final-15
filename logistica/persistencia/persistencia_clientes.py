import json
import os

from clases.cliente import Cliente
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.utils import encontrar_raiz


# ==========================================================
# NORMALIZAR TEXTO (CLAVE)
# ==========================================================
def normalizar(texto):
    return (texto or "").strip().lower()


# ==========================================================
# GUARDAR CLIENTES
# ==========================================================
def guardar_clientes(clientes_nuevos):
    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", "clientes.json")

    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    # soportar formato antiguo lista
    if isinstance(data, list):
        data = {item["dni"]: item for item in data if "dni" in item}

    for dni, c in clientes_nuevos.items():
        data[dni] = {
            "nombre": c._nombre,
            "apellidos": c._apellidos,
            "direccion": c._direccion,
            "coordenadas": c._coordenadas,

            "delegacion_cercana": (
                normalizar(c._delegacion_cercana.nombre)
                if c._delegacion_cercana else None
            ),

            "provincia": getattr(c, "_provincia", None),
            "pedidos_en_curso": c._pedidos_en_curso,
            "pedidos_terminados": c._pedidos_terminados,
            "importe_facturado": c._importe_facturado,
            "distancia_despacho": c._distancia_despacho
        }

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"✔ Clientes guardados: {len(clientes_nuevos)}")


# ==========================================================
# CARGAR CLIENTES
# ==========================================================
def cargar_clientes(nombre_fichero="clientes.json"):
    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", nombre_fichero)

    if not os.path.exists(ruta):
        return {}

    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    delegaciones = cargar_delegaciones()

    # 🔥 CLAVE: mapa NORMALIZADO
    mapa = {normalizar(d.nombre): d for d in delegaciones}

    clientes = {}

    # soportar ambos formatos
    if isinstance(data, dict):
        iterable = data.items()
    else:
        iterable = [(item.get("dni"), item) for item in data]

    for dni, item in iterable:

        if not dni:
            continue

        nombre_deleg = normalizar(item.get("delegacion_cercana"))
        deleg = mapa.get(nombre_deleg)

        c = Cliente(
            dni,
            item.get("nombre"),
            item.get("apellidos"),
            item.get("direccion"),
            deleg
        )

        coords = item.get("coordenadas")
        c._coordenadas = tuple(coords) if coords else None
        c._provincia = item.get("provincia")
        c._pedidos_en_curso = item.get("pedidos_en_curso", [])
        c._pedidos_terminados = item.get("pedidos_terminados", [])
        c._importe_facturado = item.get("importe_facturado", 0)
        c._delegacion_cercana = deleg
        c._distancia_despacho = item.get("distancia_despacho")

        clientes[dni] = c

    print(f"✔ Clientes cargados: {len(clientes)}")

    return clientes
