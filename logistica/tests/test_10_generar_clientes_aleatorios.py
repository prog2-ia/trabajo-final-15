# ==========================================================
# GENERADOR DE CLIENTES - VERSION PRO FINAL (LIMPIO)
# ==========================================================

import sys
import os
import random
import math
import folium
import webbrowser
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.geolocalizacion import direccion_cercana
from utiles.utils import distancia_km


# ==========================================================
# DATOS
# ==========================================================
nombres = [
    "Antonio", "Manuel", "José", "Francisco", "David",
    "Juan", "Javier", "Daniel", "Carlos", "Miguel",
    "Rafael", "Pedro", "Alejandro", "Luis", "Fernando",
    "Ángel", "Pablo", "Sergio", "Jorge", "Alberto",
    "Enrique", "Vicente", "Rubén", "Mario", "Iván",
    "Raúl", "Adrián", "Óscar", "Diego", "Hugo",
    "María", "Carmen", "Ana", "Isabel", "Dolores",
    "Pilar", "Laura", "Cristina", "Marta", "Lucía",
    "Sara", "Elena", "Paula", "Raquel", "Rosa",
    "Teresa", "Beatriz", "Silvia", "Patricia", "Natalia",
    "Damaris", "Julia"
]

apellidos = [
    "García", "Fernández", "González", "Rodríguez", "López",
    "Martínez", "Sánchez", "Pérez", "Gómez", "Martín",
    "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno",
    "Muñoz", "Álvarez", "Romero", "Alonso", "Gutiérrez",
    "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos",
    "Gil", "Ramírez", "Serrano", "Blanco", "Molina",
    "Morales", "Suárez", "Ortega", "Delgado", "Castro",
    "Ortiz", "Rubio", "Marín", "Sanz", "Núñez",
    "Iglesias", "Medina", "Garrido", "Cortés", "Castillo",
    "Santos", "Lozano", "Guerrero", "Cano", "Prieto", "Quiles", "Valls",
    "Borbon", "Espinosa de los Monteros"
]

def resetear_clientes():
    """
    Borra completamente el fichero de clientes.

    Se usa para empezar desde cero.
    """

    from utiles.utils import encontrar_raiz

    BASE_DIR = encontrar_raiz()
    ruta = os.path.join(BASE_DIR, "datos", "clientes.json")

    if not os.path.exists(ruta):
        print("⚠️ No existe fichero de clientes")
        return

    confirm = input("⚠️ Esto borrará TODOS los clientes. ¿Seguro? (s/n): ").lower()

    if confirm != "s":
        print("❌ Operación cancelada")
        return

    os.remove(ruta)

    print("🗑️ Fichero de clientes eliminado correctamente")

# ==========================================================
# MAPA DE CLIENTES
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

        if not hasattr(c, "_coordenadas") or not c._coordenadas:
            continue

        lat, lon = c._coordenadas

        deleg = "Sin delegación"
        if hasattr(c, "_delegacion_cercana") and c._delegacion_cercana:
            deleg = c._delegacion_cercana.nombre

        folium.Marker(
            location=[lat, lon],
            popup=f"""
            <b>{c.nombre} {c.apellidos}</b><br>
            {c.direccion}<br>
            🏢 {deleg}
            """,
            icon=folium.Icon(color="blue")
        ).add_to(mapa)

        total += 1

    if total == 0:
        print("❌ No hay clientes con coordenadas")
        return

    ruta = Path("mapa_clientes.html").resolve()
    mapa.save(ruta)

    print(f"✔ Mapa generado con {total} clientes")

    webbrowser.open(ruta.as_uri(), new=1)


# ==========================================================
# MAPA DE DELEGACIONES
# ==========================================================
def ver_mapa_delegaciones():

    print("\n🗺️ Generando mapa de delegaciones...")

    delegaciones = cargar_delegaciones()

    mapa = folium.Map(location=[39.5, -3.5], zoom_start=6)

    for d in delegaciones:

        if not d.coordenadas:
            continue

        lat, lon = d.coordenadas

        color = "blue"
        if d.__class__.__name__ == "DelegacionCentral":
            color = "red"
        elif d.__class__.__name__ == "DelegacionBase":
            color = "green"

        folium.Marker(
            location=[lat, lon],
            popup=f"{d.nombre} ({d.provincia})",
            icon=folium.Icon(color=color)
        ).add_to(mapa)

    ruta = Path("mapa_delegaciones.html").resolve()
    mapa.save(ruta)

    print(f"✔ Mapa generado: {ruta}")

    webbrowser.open(ruta.as_uri(), new=1)


# ==========================================================
# DNI
# ==========================================================
def generar_dni():
    numero = random.randint(10000000, 99999999)
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{numero}{letras[numero % 23]}"


# ==========================================================
# CONTAR CLIENTES POR DESPACHO
# ==========================================================
def contar_clientes_por_despacho(clientes):
    """
    Devuelve un diccionario con el número de clientes asociados
    a cada despacho, usando el nombre de la delegación cercana.
    """
    conteo = {}

    for c in clientes.values():
        if hasattr(c, "_delegacion_cercana") and c._delegacion_cercana:
            nombre = c._delegacion_cercana.nombre
            conteo[nombre] = conteo.get(nombre, 0) + 1

    return conteo


# ==========================================================
# GENERADOR DE CLIENTES
# ==========================================================
# ==========================================================
# GENERADOR DE CLIENTES
# ==========================================================
def generar_clientes():

    print("\n===== GENERADOR FINAL =====")

    # ==========================================================
    # CARGA DE DATOS EXISTENTES
    # ==========================================================
    clientes_existentes = cargar_clientes()
    delegaciones = cargar_delegaciones()

    # ==========================================================
    # ASEGURAR COORDENADAS DE LAS DELEGACIONES
    # ==========================================================
    for d in delegaciones:
        if not d.coordenadas:
            d.calcular_coordenadas()

    # ==========================================================
    # PEDIR PROVINCIA
    # ==========================================================
    provincia = input("\nProvincia: ").strip().lower()

    if not provincia:
        print("❌ Debes indicar una provincia")
        return

    # ==========================================================
    # FILTRAR SOLO DESPACHOS DE ESA PROVINCIA
    # ==========================================================
    despachos = []

    for d in delegaciones:

        if d.__class__.__name__ != "DelegacionDespacho":
            continue

        prov = (d.provincia or "").strip().lower()

        if prov == provincia:
            despachos.append(d)

    if not despachos:
        print("❌ No hay despachos en esa provincia")
        return

    # ==========================================================
    # CONTAR CLIENTES ACTUALES POR DESPACHO
    # ==========================================================
    conteo = contar_clientes_por_despacho(clientes_existentes)

    # ==========================================================
    # MOSTRAR DESPACHOS DISPONIBLES
    # ==========================================================
    print(f"\n🏢 DESPACHOS DE LA PROVINCIA: {provincia.upper()}\n")


    for d in despachos:
        n_clientes_actuales = conteo.get(d.nombre, 0)

        # extraer ciudad desde la dirección
        try:
            ciudad = d.direccion.split(",")[1].strip()
        except:
            ciudad = "Desconocida"

        print(f"{d.nombre} ({ciudad}) -> {n_clientes_actuales} clientes")


    # ==========================================================
    # ELEGIR DESPACHO POR NOMBRE REAL
    # ==========================================================
    try:
        numero_despacho = int(input("\nNúmero de despacho: ").strip())
    except ValueError:
        print("❌ Debes introducir un número")
        return

    nombre_buscado = f"Despacho {numero_despacho}"

    despacho = None
    for d in despachos:
        if d.nombre.strip().lower() == nombre_buscado.strip().lower():
            despacho = d
            break

    if despacho is None:
        print(f"❌ No existe {nombre_buscado} en la provincia {provincia}")
        return

    # ==========================================================
    # PEDIR NÚMERO DE CLIENTES A AÑADIR
    # ==========================================================
    try:
        n_clientes = int(input("Número de clientes a añadir: ").strip())
    except ValueError:
        print("❌ Debes introducir un número entero")
        return

    if n_clientes <= 0:
        print("❌ El número de clientes debe ser mayor que cero")
        return

    # ==========================================================
    # GENERACIÓN DE CLIENTES
    # UN SOLO INTENTO POR CADA CLIENTE PEDIDO
    # ==========================================================
    print(f"\n🏢 Generando clientes para {despacho.nombre} [{despacho.provincia}]")

    nuevos_clientes = {}
    generados = 0
    sin_direccion = 0

    lat, lon = despacho.coordenadas

    for _ in range(n_clientes):

        # ------------------------------------------------------
        # Generar una coordenada aleatoria en un radio de 1 a 4 km
        # alrededor del despacho
        # ------------------------------------------------------
        radio = random.uniform(1, 4) / 111
        t = 2 * math.pi * random.random()
        w = radio * (random.random() ** 0.5)

        coord = (
            lat + w * math.cos(t),
            lon + w * math.sin(t) / math.cos(math.radians(lat))
        )

        # ------------------------------------------------------
        # Intentar obtener una dirección cercana SOLO UNA VEZ
        # ------------------------------------------------------
        direccion = direccion_cercana(coord)

        if not direccion:
            sin_direccion += 1
            continue

        # ------------------------------------------------------
        # Generar datos personales aleatorios
        # ------------------------------------------------------
        ap1, ap2 = random.sample(apellidos, 2)
        nombre = random.choice(nombres)

        c = Cliente(
            generar_dni(),
            nombre,
            f"{ap1} {ap2}",
            direccion,
            despacho
        )

        # ------------------------------------------------------
        # Completar atributos auxiliares del cliente
        # ------------------------------------------------------
        c._coordenadas = coord
        c._provincia = despacho.provincia
        c._delegacion_cercana = despacho
        # calcular distancia al despacho
        dist = distancia_km(coord, despacho.coordenadas)

        # guardar con 2 decimales
        c._distancia_despacho = round(dist, 2)

        # ------------------------------------------------------
        # Añadir al bloque de nuevos clientes
        # ------------------------------------------------------
        nuevos_clientes[c.dni] = c
        generados += 1

    # ==========================================================
    # GUARDAR SOLO LOS NUEVOS CLIENTES
    # ==========================================================
    guardar_clientes(nuevos_clientes)

    # ==========================================================
    # RESUMEN FINAL
    # ==========================================================
    print("\n🚀 FIN GENERACIÓN")
    print(f"✔ Clientes solicitados: {n_clientes}")
    print(f"✔ Clientes generados: {generados}")
    print(f"❌ Clientes no generados por falta de dirección: {sin_direccion}")


# ==========================================================
# MOSTRAR CLIENTES
# ==========================================================
def mostrar_clientes():

    print("\n===== LISTADO CLIENTES =====")

    clientes = cargar_clientes()

    provincia = input("\nProvincia (ENTER = todas): ").strip().lower()

    total = 0

    for c in clientes.values():

        prov = (c._provincia or "").lower()

        if provincia and prov != provincia:
            continue

        print("\n-----------------------------")
        print(f"{c.nombre} {c.apellidos}")
        print(f"DNI: {c.dni}")
        print(f"Dirección: {c.direccion}")
        print(f"Provincia: {prov}")
        print(f"Delegación: {c._delegacion_cercana.nombre if c._delegacion_cercana else 'N/A'}")
        print(f"Distancia despacho: {c._distancia_despacho} km")

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
        print("6. Salir")
        print("==============================")

        op = input("Opción: ")

        if op == "1":
            generar_clientes()
        elif op == "2":
            mostrar_clientes()
        elif op == "3":
            ver_mapa_delegaciones()
        elif op == "4":
            ver_mapa_clientes()
        elif op == "5":
            resetear_clientes()
        elif op == "6":
            break
        else:
            print("❌ Opción inválida")
# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()