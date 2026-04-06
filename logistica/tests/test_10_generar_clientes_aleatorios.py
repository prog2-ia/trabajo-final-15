# ==========================================================
# GENERADOR DE CLIENTES - VERSION PRO FINAL (CORREGIDA)
# ==========================================================

import sys
import os
import random
import math

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clases.cliente import Cliente
from persistencia.persistencia_clientes import guardar_clientes, cargar_clientes
from persistencia.persistencia_delegaciones import cargar_delegaciones
from utiles.geolocalizacion import direccion_cercana


# ==========================================================
# DATOS
# ==========================================================
nombres = [
    "Antonio","Manuel","José","Francisco","David",
    "Juan","Javier","Daniel","Carlos","Miguel"
]

apellidos = [
    "García","Fernández","González","Rodríguez",
    "López","Martínez","Sánchez","Pérez"
]


# ==========================================================
# DNI
# ==========================================================
def generar_dni():
    numero = random.randint(10000000, 99999999)
    letras = "TRWAGMYFPDXBNJZSQVHLCKE"
    return f"{numero}{letras[numero % 23]}"


# ==========================================================
# GENERADOR
# ==========================================================
def generar_clientes():

    print("\n===== GENERADOR FINAL =====")

    opcion = input("¿Generar desde cero (s) o añadir (n)? ").lower()

    if opcion == "s":
        clientes = {}
    else:
        clientes = cargar_clientes()

    provincia = input("\nProvincia (ENTER = todas): ").strip().lower()

    n_clientes = int(input("Clientes por delegación: "))
    max_intentos = int(input("Máximo de intentos: "))

    delegaciones = cargar_delegaciones()

    # asegurar coordenadas
    for d in delegaciones:
        if not d.coordenadas:
            d.calcular_coordenadas()

    # ======================================================
    # FILTRADO
    # ======================================================
    print("\n🔎 FILTRANDO DESPACHOS...\n")

    despachos = []

    for d in delegaciones:

        if d.__class__.__name__ != "DelegacionDespacho":
            continue

        prov = (d.provincia or "").lower()

        print(f"🏢 {d.nombre}")
        print(f"   Provincia: {prov}")

        if provincia and prov != provincia:
            print("   ❌ Excluido\n")
            continue

        print("   ✔ Incluido\n")
        despachos.append(d)

    if not despachos:
        print("❌ No hay despachos")
        return

    print("\n📍 DESPACHOS SELECCIONADOS:\n")

    for d in despachos:
        print(f"- {d.nombre} ({d.provincia})")

    # ======================================================
    # GENERACIÓN
    # ======================================================
    for d in despachos:

        print("\n==============================")
        print(f"🏢 {d.nombre} [{d.provincia}]")
        print("==============================\n")

        generados = 0
        intentos = 0

        while generados < n_clientes and intentos < max_intentos:

            intentos += 1

            print(f"\r🔄 Intento {intentos}/{max_intentos} | Generados: {generados}", end="")

            lat, lon = d.coordenadas

            # generar punto aleatorio cercano
            radio = random.uniform(1, 4) / 111
            t = 2 * math.pi * random.random()
            w = radio * (random.random() ** 0.5)

            coord = (
                lat + w * math.cos(t),
                lon + w * math.sin(t) / math.cos(math.radians(lat))
            )

            print(f"\n   📍 Coordenada: {coord}")

            direccion = direccion_cercana(coord)

            if not direccion:
                print("   ❌ No geolocalizado")
                continue

            print(f"   📬 Dirección: {direccion}")

            ap1 = random.choice(apellidos)
            ap2 = random.choice(apellidos)

            if ap1 == ap2:
                print("   ❌ Apellidos iguales")
                continue

            nombre = random.choice(nombres)

            print("   👤 Creando cliente...")
            print(f"   🏢 Delegación asignada: {d.nombre}")

            c = Cliente(
                generar_dni(),
                nombre,
                f"{ap1} {ap2}",
                direccion,
                d
            )

            # atributos extra
            c._coordenadas = coord
            c._provincia = d.provincia
            c.delegacion_cercana = d   # 🔥 CLAVE

            clientes[c.dni] = c

            generados += 1

        print(f"\n✔ Generados en {d.nombre}: {generados}")

    guardar_clientes(clientes)

    print("\n🚀 FIN GENERACIÓN")


# ==========================================================
# MOSTRAR CLIENTES
# ==========================================================
def mostrar_clientes():

    print("\n===== LISTADO RÁPIDO DE CLIENTES =====")

    clientes = cargar_clientes()

    provincia = input("\nProvincia (ENTER = todas): ").strip().lower()

    total = 0

    for c in clientes.values():

        prov = (c._provincia or "").lower()

        if provincia and prov != provincia:
            continue

        print("\n-----------------------------------")
        print(f"DNI: {c.dni}")
        print(f"{c.nombre} {c.apellidos}")
        print(f"📍 {c.direccion}")
        print(f"🌍 {prov}")

        # delegación segura
        deleg = None

        if hasattr(c, "delegacion_cercana") and c.delegacion_cercana:
            if hasattr(c.delegacion_cercana, "nombre"):
                deleg = c.delegacion_cercana.nombre
            else:
                deleg = str(c.delegacion_cercana)

        if not deleg:
            deleg = "Sin delegación"

        print(f"🏢 {deleg}")

        total += 1

    print("\n===================================")
    print(f"TOTAL: {total}")


# ==========================================================
# MENU
# ==========================================================
def menu():

    while True:

        print("\n==============================")
        print("1. Generar clientes")
        print("2. Ver clientes")
        print("3. Salir")
        print("==============================")

        op = input("Opción: ")

        if op == "1":
            generar_clientes()
        elif op == "2":
            mostrar_clientes()
        elif op == "3":
            break
        else:
            print("❌ Opción inválida")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    menu()