# ==========================================================
# GENERADOR DE CLIENTES - VERSION PRO FINAL (CORREGIDO)
# ==========================================================

import math
import os
import random
import sys
import webbrowser
from utiles.utils import encontrar_raiz

import folium

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.geolocalizacion import direccion_cercana
from utiles.utils import distancia_km


# ==========================================================
# DATOS
# ==========================================================
nombres = [...]
apellidos = [...]

# ==========================================================
# RESETEAR CLIENTES
# ==========================================================
def resetear_clientes():

    base_dir = encontrar_raiz()
    ruta = os.path.join(base_dir, "datos", "clientes.json")

    if not os.path.exists(ruta):
        print("⚠️ No existe fichero de clientes")
        return

    confirm = input("⚠️ Esto borrará TODOS los clientes. ¿Seguro? (s/n): ").strip().lower()

    if confirm != "s":
        print("❌ Operación cancelada")
        return

    os.remove(ruta)
    print("🗑️ Fichero de clientes eliminado correctamente")


# ==========================================================
# LIMPIAR CLIENTES SIN GEO
# ==========================================================
def limpiar_clientes_sin_geo():

    print("\n🧹 LIMPIEZA DE CLIENTES SIN GEO")

    clientes = cargar_clientes()

    if not clientes:
        print("❌ No hay clientes")
        return

    total = len(clientes)
    eliminados = 0

    clientes_filtrados = {}

    for dni, c in clientes.items():

        poblacion_real = getattr(c, "_poblacion", None)
        provincia_real = getattr(c, "_provincia", None)

        if not poblacion_real or not provincia_real:
            print(f"❌ Eliminado: {c.nombre} {c.apellidos} ({dni})")
            eliminados += 1
            continue

        clientes_filtrados[dni] = c

    guardar_clientes(clientes_filtrados, sobrescribir=True)

    print("\n✔ LIMPIEZA COMPLETADA")
    print(f"Total clientes: {total}")
    print(f"Eliminados: {eliminados}")
    print(f"Restantes: {len(clientes_filtrados)}")

# ==========================================================
# MAPA DE DELEGACIONES
# ==========================================================
def ver_mapa_delegaciones():

    print("\n🗺️ Generando mapa de delegaciones...")

    delegaciones = cargar_delegaciones()

    if not delegaciones:
        print("❌ No hay delegaciones")
        return

    mapa = folium.Map(location=[39.5, -3.5], zoom_start=6)

    total = 0

    for d in delegaciones:

        if not d.coordenadas:
            continue

        lat, lon = d.coordenadas

        # color según tipo
        color = "blue"

        if d.__class__.__name__ == "DelegacionCentral":
            color = "red"
        elif d.__class__.__name__ == "DelegacionBase":
            color = "green"
        elif d.__class__.__name__ == "DelegacionDespacho":
            color = "blue"

        folium.Marker(
            location=[lat, lon],
            popup=f"""
            <b>{d.nombre}</b><br>
            {d.direccion}<br>
            🗺️ {d.provincia}
            """,
            icon=folium.Icon(color=color)
        ).add_to(mapa)

        total += 1

    if total == 0:
        print("❌ No hay delegaciones con coordenadas")
        return

    base_dir = encontrar_raiz()
    ruta = os.path.join(base_dir, "datos", "mapa_delegaciones.html")

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    mapa.save(ruta)

    print(f"✔ Mapa guardado en: {ruta}")
    webbrowser.open(f"file://{ruta}")

# ==========================================================
# MAPA CLIENTES
# ==========================================================
def ver_mapa_clientes():

    print("\n🗺️ Generando mapa de clientes...")

    clientes = cargar_clientes()

    if not clientes:
        print("❌ No hay clientes")
        return

    mapa = folium.Map(location=[39.5, -3.5], zoom_start=6)

    total = 0

    for c in clientes.values():

        if not c._coordenadas:
            continue

        lat, lon = c._coordenadas

        deleg = c._delegacion_cercana.nombre if c._delegacion_cercana else "Sin delegación"

        folium.Marker(
            location=[lat, lon],
            popup=f"<b>{c.nombre} {c.apellidos}</b><br>{c.direccion}<br>🏢 {deleg}",
            icon=folium.Icon(color="blue")
        ).add_to(mapa)

        total += 1

    if total == 0:
        print("❌ No hay clientes con coordenadas")
        return

    base_dir = encontrar_raiz()
    ruta = os.path.join(base_dir, "datos", "mapa_clientes.html")

    os.makedirs(os.path.dirname(ruta), exist_ok=True)

    mapa.save(ruta)

    print(f"✔ Mapa guardado en: {ruta}")
    webbrowser.open(f"file://{ruta}")


# ==========================================================
# GENERADOR CLIENTES
# ==========================================================
def generar_clientes():

    print("\n===== GENERADOR FINAL =====")

    clientes_existentes = cargar_clientes()
    delegaciones = cargar_delegaciones()

    provincia = input("\nProvincia: ").strip().lower()

    despachos = [
        d for d in delegaciones
        if d.__class__.__name__ == "DelegacionDespacho"
        and (d.provincia or "").lower() == provincia
    ]

    if not despachos:
        print("❌ No hay despachos")
        return

    for d in despachos:
        print(d.nombre)

    numero = int(input("\nNúmero despacho: "))
    despacho = next((d for d in despachos if f"Despacho {numero}".lower() in d.nombre.lower()), None)

    if not despacho:
        print("❌ No encontrado")
        return

    n_clientes = int(input("Número clientes: "))

    nuevos_clientes = {}
    generados = 0

    lat, lon = despacho.coordenadas

    for i in range(n_clientes):

        radio = random.uniform(1, 4) / 111
        t = 2 * math.pi * random.random()
        w = radio * (random.random() ** 0.5)

        coord = (
            lat + w * math.cos(t),
            lon + w * math.sin(t) / math.cos(math.radians(lat))
        )

        direccion = direccion_cercana(coord)

        if not direccion:
            continue

        nombre = random.choice(nombres)
        ap1, ap2 = random.choices(apellidos, k=2)

        dni = str(random.randint(10000000, 99999999))

        c = Cliente(dni, nombre, f"{ap1} {ap2}", direccion)
        c._coordenadas = coord

        # GEO
        c.actualizar_datos_geo()

        print("\n🔎 DEBUG GEO:")
        print(f"📍 {coord}")
        print(f"🏠 {direccion}")
        print(f"🌆 {c.poblacion}")
        print(f"🗺️ {c.provincia}")
        print("-" * 40)

        # VALIDACIÓN
        if not getattr(c, "_poblacion", None) or not getattr(c, "_provincia", None):
            print("❌ descartado")
            continue

        c._delegacion_cercana = despacho
        c._distancia_despacho = round(distancia_km(coord, despacho.coordenadas), 2)

        nuevos_clientes[dni] = c
        generados += 1

    if nuevos_clientes:
        guardar_clientes(nuevos_clientes)

    print(f"\n✔ Generados: {generados}")
# ==========================================================
# MOSTRAR CLIENTES
# ==========================================================
def mostrar_clientes():
    """
    Muestra los clientes almacenados con opción de filtrar por provincia.
    Compatible con nuevos campos (_poblacion, _provincia, distancia).
    """

    print("\n===== LISTADO CLIENTES =====")

    clientes = cargar_clientes()

    if not clientes:
        print("❌ No hay clientes guardados")
        return

    provincia_filtro = input("\nProvincia (ENTER = todas): ").strip().lower()

    total = 0

    # Cabecera
    print(
        f"{'DNI':<12}"
        f"{'NOMBRE':<28}"
        f"{'DIRECCIÓN':<40}"
        f"{'POBLACIÓN':<15}"
        f"{'PROVINCIA':<15}"
        f"{'KM':>6}"
    )
    print("-" * 116)

    for c in clientes.values():

        # ------------------------------------------------------
        # PROVINCIA (robusta)
        # ------------------------------------------------------
        prov = ""

        if hasattr(c, "provincia") and c.provincia:
            prov = c.provincia.lower()
        elif hasattr(c, "_provincia") and c._provincia:
            prov = c._provincia.lower()

        # filtro
        if provincia_filtro and prov != provincia_filtro:
            continue

        # ------------------------------------------------------
        # DATOS
        # ------------------------------------------------------
        nombre = f"{c.apellidos}, {c.nombre}"
        direccion = c.direccion or "N/A"

        poblacion = (
            c.poblacion if hasattr(c, "poblacion") and c.poblacion
            else getattr(c, "_poblacion", "N/A")
        )

        provincia = (
            c.provincia if hasattr(c, "provincia") and c.provincia
            else getattr(c, "_provincia", "N/A")
        )

        distancia = (
            f"{c._distancia_despacho:.2f}"
            if hasattr(c, "_distancia_despacho") and c._distancia_despacho
            else "N/A"
        )

        # ------------------------------------------------------
        # RECORTES (para que no rompa tabla)
        # ------------------------------------------------------
        nombre = nombre[:27]
        direccion = direccion[:39]
        poblacion = poblacion[:14] if poblacion else "N/A"
        provincia = provincia[:14] if provincia else "N/A"

        # ------------------------------------------------------
        # PRINT
        # ------------------------------------------------------
        print(
            f"{c.dni:<12}"
            f"{nombre:<28}"
            f"{direccion:<40}"
            f"{poblacion:<15}"
            f"{provincia:<15}"
            f"{distancia:>6}"
        )

        total += 1

    print(f"\nTOTAL: {total}")
# ==========================================================
# MENU
# ==========================================================
def ejecutar():

    print("\n" + "*" * 40)
    print("   GENERACION DE DATOS DE PRUEBA DE CLIENTES CON GEOLOCALIZACIÓN")
    print("*" * 40)

    while True:

        print("\n==============================")
        print("1. Generar clientes")
        print("2. Ver clientes")
        print("3. Ver mapa delegaciones")
        print("4. Ver mapa clientes")
        print("5. 🔥 Resetear clientes (borrar fichero)")
        print("6. 🧹 Borrar clientes sin poblacion/provincia")
        print("0. Salir")
        print("==============================")

        op = input("Opción: ").strip()

        if op == "1":
            generar_clientes()

        elif op == "2":
            mostrar_clientes()   # 🔥 IMPORTANTE

        elif op == "3":
            ver_mapa_delegaciones()

        elif op == "4":
            ver_mapa_clientes()

        elif op == "5":
            resetear_clientes()   # 🔥 IMPORTANTE

        elif op == "6":
            limpiar_clientes_sin_geo()   # 🔥 NUEVO

        elif op == "0":
            break

        else:
            print("❌ Opción inválida")
