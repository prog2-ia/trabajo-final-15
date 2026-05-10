"""
==========================================================
MÓDULO: mantenimiento_delegaciones.py
==========================================================

Mantenimiento completo de delegaciones logísticas.

FUNCIONALIDADES:
✔ Altas
✔ Modificaciones
✔ Bajas
✔ Listados jerárquicos

CARACTERÍSTICAS:
✔ Validación de nombres únicos
✔ Validación de delegación superior
✔ Geolocalización automática
✔ Extracción de población y provincia
✔ Persistencia JSON
✔ Gestión jerárquica

ARQUITECTURA:
Central → Base → Despacho
"""

# ==========================================================
# IMPORTS
# ==========================================================
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from clases.delegacion import (
    DelegacionCentral,
    DelegacionBase,
    DelegacionDespacho
)

from persistencia.persistencia_delegaciones import (
    guardar_delegaciones,
    cargar_delegaciones
)

from utiles.geolocalizacion import (
    geocodificar,
    obtener_datos_geo
)


# ==========================================================
# BUSCAR DELEGACIÓN
# ==========================================================
def buscar_delegacion(nombre, delegaciones):

    for d in delegaciones:

        if d.nombre.lower() == nombre.lower():
            return d

    return None


# ==========================================================
# GENERAR NOMBRE POR DEFECTO
# ==========================================================
def generar_nombre(tipo, delegaciones):

    prefijo = tipo.capitalize()

    numeros = []

    for d in delegaciones:

        if d.nombre.startswith(prefijo):

            partes = d.nombre.split()

            if len(partes) >= 2:

                if partes[-1].isdigit():
                    numeros.append(int(partes[-1]))

    siguiente = max(numeros, default=0) + 1

    return f"{prefijo} {siguiente}"


# ==========================================================
# SELECCIONAR DELEGACIÓN SUPERIOR
# ==========================================================
# ==========================================================
# SELECCIONAR DELEGACIÓN SUPERIOR
# ==========================================================
def seleccionar_superior(tipo, delegaciones):

    # ======================================================
    # BASE → depende de CENTRAL
    # ======================================================
    if tipo == "base":

        candidatos = [

            d for d in delegaciones

            if isinstance(
                d,
                DelegacionCentral
            )
        ]

        texto = "central"

    # ======================================================
    # DESPACHO → depende de BASE
    # ======================================================
    elif tipo == "despacho":

        candidatos = [

            d for d in delegaciones

            if isinstance(
                d,
                DelegacionBase
            )
        ]

        texto = "base"

    else:

        return None

    # ======================================================
    # VALIDAR EXISTENCIA
    # ======================================================
    if not candidatos:

        print(
            f"\n❌ No existen {texto}s"
        )

        return None

    # ======================================================
    # MOSTRAR OPCIONES
    # ======================================================
    print(f"\n{texto.upper()}S DISPONIBLES:\n")

    for i, d in enumerate(
            candidatos,
            start=1
    ):

        print(
            f"{i}. {d.nombre}"
        )

    # ======================================================
    # PEDIR SELECCIÓN
    # ======================================================
    while True:

        entrada = input(
            f"\nSeleccione {texto}: "
        ).strip()

        # --------------------------------------------------
        # POR NÚMERO
        # --------------------------------------------------
        if entrada.isdigit():

            indice = int(entrada)

            if 1 <= indice <= len(candidatos):

                return candidatos[indice - 1]

        # --------------------------------------------------
        # POR NOMBRE
        # --------------------------------------------------
        for d in candidatos:

            if d.nombre.lower() == entrada.lower():

                return d

        print(
            f"\n❌ {texto.capitalize()} inválida"
        )

# ==========================================================
# PEDIR DIRECCIÓN GEOLOCALIZADA
# ==========================================================
def pedir_direccion():

    while True:

        direccion = input(
            "\nDirección completa: "
        ).strip()

        try:

            coord = geocodificar(direccion)

            if not coord:

                print(
                    "\n❌ No se pudo geolocalizar"
                )

                continue

            poblacion, provincia = (
                obtener_datos_geo(coord)
            )

            print("\n✔ Dirección válida")
            print(f"Población: {poblacion}")
            print(f"Provincia: {provincia}")

            return (
                direccion,
                coord,
                poblacion,
                provincia
            )

        except Exception as e:

            print(f"\n❌ Error: {e}")


# ==========================================================
# ALTAS
# ==========================================================
def alta_delegacion(delegaciones):

    print("\n" + "=" * 50)
    print("ALTA DE DELEGACIÓN")
    print("=" * 50)

    # ------------------------------------------------------
    # TIPO
    # ------------------------------------------------------
    print("\n1. Central")
    print("2. Base")
    print("3. Despacho")

    opcion = input("\nSeleccione tipo: ")

    tipos = {
        "1": "central",
        "2": "base",
        "3": "despacho"
    }

    if opcion not in tipos:

        print("\n❌ Tipo inválido")
        return

    tipo = tipos[opcion]

    # ------------------------------------------------------
    # SUPERIOR
    # ------------------------------------------------------
    superior = seleccionar_superior(
        tipo,
        delegaciones
    )

    # ------------------------------------------------------
    # NOMBRE
    # ------------------------------------------------------
    nombre_default = generar_nombre(
        tipo,
        delegaciones
    )

    while True:

        nombre = input(
            f"\nNombre [{nombre_default}]: "
        ).strip()

        if not nombre:
            nombre = nombre_default

        if buscar_delegacion(
                nombre,
                delegaciones
        ):

            print(
                "\n❌ Ya existe una delegación "
                "con ese nombre"
            )

            continue

        break

    # ------------------------------------------------------
    # DIRECCIÓN
    # ------------------------------------------------------
    (
        direccion,
        coord,
        poblacion,
        provincia
    ) = pedir_direccion()

    # ------------------------------------------------------
    # CREAR OBJETO
    # ------------------------------------------------------
    if tipo == "central":

        d = DelegacionCentral(
            nombre,
            direccion,
            provincia=provincia,
            poblacion=poblacion,
            coordenadas=coord
        )

    elif tipo == "base":

        d = DelegacionBase(
            nombre,
            direccion,
            delegacion_superior=superior,
            provincia=provincia,
            poblacion=poblacion,
            coordenadas=coord
        )

    else:

        d = DelegacionDespacho(
            nombre,
            direccion,
            delegacion_superior=superior,
            provincia=provincia,
            poblacion=poblacion,
            coordenadas=coord
        )

    delegaciones.append(d)

    guardar_delegaciones(delegaciones)

    print("\n✔ Delegación creada")


# ==========================================================
# MODIFICACIONES
# ==========================================================
def modificar_delegacion(delegaciones):

    print("\n" + "=" * 50)
    print("MODIFICACIÓN DE DELEGACIÓN")
    print("=" * 50)

    nombre = input(
        "\nNombre delegación: "
    )

    d = buscar_delegacion(
        nombre,
        delegaciones
    )

    if not d:

        print("\n❌ Delegación no encontrada")
        return

    print("\nDATOS ACTUALES\n")

    print(f"Nombre: {d.nombre}")
    print(f"Dirección: {d.direccion}")
    print(f"Población: {d.poblacion}")
    print(f"Provincia: {d.provincia}")

    # ------------------------------------------------------
    # NOMBRE
    # ------------------------------------------------------
    while True:

        nuevo_nombre = input(
            f"\nNombre [{d.nombre}]: "
        ).strip()

        if not nuevo_nombre:
            nuevo_nombre = d.nombre

        existe = buscar_delegacion(
            nuevo_nombre,
            delegaciones
        )

        if existe and existe != d:

            print("\n❌ Nombre duplicado")
            continue

        break

    # ------------------------------------------------------
    # DIRECCIÓN
    # ------------------------------------------------------
    direccion = input(
        f"\nDirección [{d.direccion}]: "
    ).strip()

    if not direccion:

        direccion = d.direccion
        coord = d.coordenadas
        poblacion = d.poblacion
        provincia = d.provincia

    else:

        (
            direccion,
            coord,
            poblacion,
            provincia
        ) = pedir_direccion()

    # ------------------------------------------------------
    # ACTUALIZAR
    # ------------------------------------------------------
    d._nombre = nuevo_nombre
    d._direccion = direccion
    d._coordenadas = coord
    d._poblacion = poblacion
    d._provincia = provincia

    guardar_delegaciones(delegaciones)

    print("\n✔ Delegación modificada")


# ==========================================================
# BAJAS
# ==========================================================
def baja_delegacion(delegaciones):

    print("\n" + "=" * 50)
    print("BAJA DE DELEGACIÓN")
    print("=" * 50)

    nombre = input(
        "\nNombre delegación: "
    )

    d = buscar_delegacion(
        nombre,
        delegaciones
    )

    if not d:

        print("\n❌ Delegación no encontrada")
        return

    print("\nDelegación encontrada:")
    print(d)

    confirmar = input(
        "\n¿Confirmar baja? (s/n): "
    ).lower()

    if confirmar != "s":

        print("\n✔ Operación cancelada")
        return

    delegaciones.remove(d)

    guardar_delegaciones(delegaciones)

    print("\n✔ Delegación eliminada")



# ==========================================================
# IMPRIMIR JERARQUÍA
# ==========================================================
def imprimir_jerarquia(delegaciones):

    # ======================================================
    # CONFIGURACIÓN DE COLUMNAS
    # ======================================================
    ANCHO_NOMBRE = 35

    # ======================================================
    # FUNCIÓN AUXILIAR
    # ======================================================
    def imprimir_linea(prefijo, delegacion):

        nombre = f"{prefijo}{delegacion.nombre}"

        print(
            f"{nombre:<{ANCHO_NOMBRE}}"
            f"│ Dirección: {delegacion.direccion} "
            f"│ Población: {delegacion.poblacion} "
            f"│ Provincia: {delegacion.provincia}"
        )

    # ======================================================
    # CENTRALES
    # ======================================================
    centrales = [

        d for d in delegaciones

        if isinstance(d, DelegacionCentral)
    ]

    for central in centrales:

        imprimir_linea(
            "",
            central
        )

        # ==================================================
        # BASES
        # ==================================================
        bases = [

            d for d in delegaciones

            if isinstance(d, DelegacionBase)

            and d.delegacion_superior == central
        ]

        for b in bases:

            imprimir_linea(
                "   ├── ",
                b
            )

            # ==============================================
            # DESPACHOS
            # ==============================================
            despachos = [

                d for d in delegaciones

                if isinstance(
                    d,
                    DelegacionDespacho
                )

                and d.delegacion_superior == b
            ]

            for dep in despachos:

                imprimir_linea(
                    "   │     ├── ",
                    dep
                )
# ==========================================================
# LISTADOS
# ==========================================================
def listado_delegaciones(delegaciones):
    '''
    print("\n" + "=" * 50)
    print("LISTADO DE DELEGACIONES")
    print("=" * 50)

    print("\n1. Todas")
    print("2. Por provincia")
    print("3. Por población")

    opcion = input("\nSeleccione opción: ")

    resultado = delegaciones

    # ------------------------------------------------------
    # FILTRAR PROVINCIA
    # ------------------------------------------------------
    if opcion == "2":

        provincia = input(
            "\nProvincia: "
        ).lower()

        resultado = [

            d for d in delegaciones

            if d.provincia
            and d.provincia.lower() == provincia
        ]

    # ------------------------------------------------------
    # FILTRAR POBLACIÓN
    # ------------------------------------------------------
    elif opcion == "3":

        poblacion = input(
            "\nPoblación: "
        ).lower()

        resultado = [

            d for d in delegaciones

            if d.poblacion
            and d.poblacion.lower() == poblacion
        ]
    '''

    # ------------------------------------------------------
    # MOSTRAR
    # ------------------------------------------------------
    #   imprimir_jerarquia(resultado)
    imprimir_jerarquia(delegaciones)


# ==========================================================
# MENÚ PRINCIPAL
# ==========================================================
def ejecutar():

    delegaciones = cargar_delegaciones()

    while True:

        print("\n" + "=" * 60)
        print("MANTENIMIENTO DE DELEGACIONES")
        print("=" * 60)

        print("\n1. Alta")
        print("2. Modificación")
        print("3. Baja")
        print("4. Listado")
        print("5. Salir")

        opcion = input("\nSeleccione opción: ")

        # --------------------------------------------------
        # ALTAS
        # --------------------------------------------------
        if opcion == "1":

            alta_delegacion(
                delegaciones
            )

        # --------------------------------------------------
        # MODIFICACIÓN
        # --------------------------------------------------
        elif opcion == "2":

            modificar_delegacion(
                delegaciones
            )

        # --------------------------------------------------
        # BAJAS
        # --------------------------------------------------
        elif opcion == "3":

            baja_delegacion(
                delegaciones
            )

        # --------------------------------------------------
        # LISTADOS
        # --------------------------------------------------
        elif opcion == "4":

            listado_delegaciones(
                delegaciones
            )

        # --------------------------------------------------
        # SALIR
        # --------------------------------------------------
        elif opcion == "5":

            break

        else:

            print("\n❌ Opción inválida")


# ==========================================================
# MAIN
# ==========================================================
if __name__ == "__main__":
    ejecutar()
